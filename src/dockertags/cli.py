#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get image Tags from Docker Hub

this file is copied from https://github.com/yolabingo/dockertags/blob/main/src/dockertags/cli.py
"""
import argparse
import json
import warnings
from datetime import datetime

import pkg_resources
import requests


class DockerhubTags:
    """
    provide sorting/comparison based on a tag's name and `last_updated` values
    """

    def __init__(self, name, last_updated=None):
        """
        self.version strips everything after [_-] as it is ignored by pkg_resources.parse_version
        """
        big_version = "999999999999"
        self.name = name
        if name == "latest":
            self.version = pkg_resources.parse_version(big_version)
        else:
            ## suppress "PkgResourcesDeprecationWarning: XXX is an invalid version and will not be supported in a future release"
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.version = pkg_resources.parse_version(
                    name.split("_")[0].split("-")[0]
                )
        # Dockerhub API format: "last_updated": "2022-10-17T23:19:38.986447Z"
        try:
            isoformat = last_updated.split(".")[0]
        except AttributeError:
            isoformat = "2000-01-01T00:00:00"
        self.last_updated = datetime.fromisoformat(isoformat)

    def _versions_eq(self, other):
        return self.version == other.version

    def _versions_lt(self, other):
        if self._versions_eq(other):
            return False
        return self.version < other.version

    def _last_updated_eq(self, other):
        return self.last_updated == other.last_updated

    def _last_updated_lt(self, other):
        return self.last_updated < other.last_updated

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        if self._versions_eq(other):
            return self._last_updated_lt(other)
        if self._versions_lt(other):
            return True
        return False

    def __str__(self):
        return self.name


class GetDockerhubTags:
    """gets tags for dockerhub repos"""

    def __init__(
        self,
        namespace,
        repository,
        max_results=None,
        exclude_substrings=None,
        include_substrings=None,
        min_version=None,
        max_version=None,
    ):
        """
        query dockerhub API for specified dockerhub namespace and respository
        set page_limit as large repos are... large
        """
        self.tags = []
        self.repository = repository
        self.namespace = namespace
        self.exclude_substrings = exclude_substrings
        self.include_substrings = include_substrings
        self.page_size = 100  # dockerhub api max
        if max_results is None:
            max_results = 2000
        self.page_limit = int((max_results - 1) / self.page_size)
        if min_version is None:
            self.min_version = None
        else:
            self.min_version = DockerhubTags(min_version)
        if max_version is None:
            self.max_version = None
        else:
            self.max_version = DockerhubTags(max_version)

    def _get_url(self, page=1):
        return f"https://hub.docker.com/v2/namespaces/{self.namespace}/repositories/{self.repository}/tags?page={page}&page_size={self.page_size}"

    def _exclude_tag(self, tag):
        """
        exclude tags containing provided substrings
        returns True if provided tag should be excluded
        """
        if self.exclude_substrings:
            for exclude in self.exclude_substrings:
                if exclude in tag:
                    return True
        return False

    def _include_tag(self, tag):
        """
        include tags containing provided substrings
        returns True if provided tag should be included
        """
        # do no checks if self.include_substrings is None
        if self.include_substrings is None:
            return True
        for include in self.include_substrings:
            if include in tag:
                return True
        return False

    def _under_page_limit(self, url):
        """
        if 'page=n' query string value is less than self.page_limit, return url
        else, return None
        """
        qs = url.split("?")[1]
        for arg in qs.split("&"):
            name, value = arg.split("=")
            if name == "page" and (int(value) < self.page_limit):
                return url
        return None

    def _save_tag(self, name, last_updated):
        if self._exclude_tag(name):
            return None
        if not self._include_tag(name):
            return None
        tag = DockerhubTags(name, last_updated)
        if (self.min_version is not None) and (tag < self.min_version):
            return None
        if (self.max_version is not None) and (tag > self.max_version):
            return None
        self.tags.append(tag)

    def _get_page(self, url):
        """
        requests a single "tags" page from Dockerhub API
        Adds found tags to self.tags list
        Returns next page URL of paginated results, if exists
        """
        next_page_url = None
        tags = set()
        response = requests.get(url)
        if response.status_code == 200:
            response_body = json.loads(response.text)
            next_page_url = response_body["next"]
            for result in response_body["results"]:
                self._save_tag(result["name"], result["last_updated"])
        else:
            print(url)
            print(f"Code: {response.status_code}")
        return next_page_url

    def get_tags(self):
        next_page = self._get_url()
        # starting a page 1, loop through paginated results
        while next_page:
            next_page = self._get_page(next_page)
            if next_page:
                next_page = self._under_page_limit(next_page)
        self.tags.sort()
        return self.tags


def cli():
    parser = argparse.ArgumentParser(
        description="Gets Tags for a Docker Hub repository"
    )
    parser.add_argument(
        "namespace",
        type=str,
        help="Docker Hub namespace",
    )
    parser.add_argument(
        "repository",
        type=str,
        help="Docker Hub repository",
    )
    parser.add_argument(
        "--exclude-substrings",
        "-x",
        type=str,
        nargs="+",
        help="Tags containing these substrings will be excluded, e.g. 'SNAPSHOT test'",
    )
    parser.add_argument(
        "--include-substrings",
        "-i",
        type=str,
        nargs="+",
        help="Tags containing these substrings will be included, e.g. 'lts debian'",
    )
    parser.add_argument(
        "--min-version",
        "-v",
        type=str,
        default=None,
        help="Minimum included version number",
    )
    parser.add_argument(
        "--max-version",
        "-w",
        type=str,
        default=None,
        help="Maximum included version number",
    )
    parser.add_argument(
        "--max-results",
        "-m",
        type=int,
        default=None,
        help="Maximum number of results to pull, default=2000",
    )
    args = parser.parse_args()

    dockerhub_tags = GetDockerhubTags(
        args.namespace,
        args.repository,
        exclude_substrings=args.exclude_substrings,
        include_substrings=args.include_substrings,
        min_version=args.min_version,
        max_version=args.max_version,
        max_results=args.max_results,
    )
    tags = dockerhub_tags.get_tags()
    for tag in tags:
        print(tag)


if __name__ == "__main__":
    cli()
