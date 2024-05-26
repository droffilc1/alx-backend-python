#!/usr/bin/env python3
"""test_client
Implements unit test for client.
"""
import unittest
from typing import Any, Dict
from unittest.mock import PropertyMock, patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit test for GithubOrgClient."""
    @parameterized.expand([
        ('google',),
        ('abc',)
    ])
    @patch('client.get_json')
    def test_org(self, org: str, mock_get: Any) -> None:
        """Test that GithubOrgClient.org returns the correct value."""
        test_class = GithubOrgClient(org)
        test_class.org()
        mock_get.assert_called_once_with(test_class.ORG_URL.format(org=org))

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org: PropertyMock) -> None:
        """Tests `GithubOrgClient._public_repos_url` method."""
        # Define a known payload for mocking
        mock_payload: Dict[str, str] = {
            "repos_url": "https://api.github.com/orgs/test_org/repos"
        }
        # Set the mock to return the known payload
        mock_org.return_value = mock_payload

        # Instantiate the client
        client = GithubOrgClient('test_org')

        # Assert that _public_repos_url return the expected repos_url
        expected_url: str = mock_payload['repos_url']
        self.assertEqual(client._public_repos_url, expected_url)


if __name__ == '__main__':
    unittest.main()
