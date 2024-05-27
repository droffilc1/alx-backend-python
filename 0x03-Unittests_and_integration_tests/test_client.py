#!/usr/bin/env python3
"""test_client
Implements unit test for client.
"""
import unittest
from typing import Any, Dict, List
from unittest.mock import Mock, PropertyMock, patch
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


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
        # source:
        # https://stackoverflow.com/questions/11836436/how-to-mock-a-\
        # readonly-property-with-mock
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

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url',
           new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url: PropertyMock,
                          mock_get_json: Any) -> None:
        """Test `GithubOrgClient.public_repos` method."""
        # Define a known payload for the mocked _public_repos_url
        mock_public_repos_url.return_value = \
            "https://api.github.com/orgs/test_org/repos"

        # Define a known payload for the mocked get_json
        mock_repos_payload: List[Dict[str, Any]] = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}},
        ]
        mock_get_json.return_value = mock_repos_payload

        # Instantiate the client
        client = GithubOrgClient("test_org")

        # Call the public_repos method and assert the expected result
        expected_repos_mit: List[str] = ["repo1", "repo2", "repo3"]
        self.assertEqual(client.public_repos(), expected_repos_mit)

        # Test with a specific license filter
        expected_repos_mit: List[str] = ["repo1", "repo3"]
        self.assertEqual(client.public_repos(
            license="mit"), expected_repos_mit)

        # Assert that the mocked property and the mocked get_json were
        # called once
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/test_org/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict[str, Any],
                         license_key: str, expected: bool) -> None:
        """Tests `GithubOrgClient.has_license` method."""
        # Instantiate the client
        client = GithubOrgClient("test_org")

        # Call the has_license method with the given parameters and
        # assert the result
        self.assertEqual(client.has_license(repo, license_key), expected)

    @parameterized_class([
        {
            'org_payload': TEST_PAYLOAD[0][0],
            'repos_payload': TEST_PAYLOAD[0][1],
            'expected_repos': TEST_PAYLOAD[0][2],
            'apache_repos': TEST_PAYLOAD[0][3]
        }
    ])
    class TestIntegrationGithubOrgClient(unittest.TestCase):
        """Implements the setUpClass and tearDownClass."""

        # Define dummy attributes to satisfy pylint
        org_payload = {}
        repos_payload = []
        expected_repos = []
        apache2_repos = []

        @classmethod
        def setUpClass(cls) -> None:
            """Set up the class by mocking request.get."""
            route_payload = {
                'https://api.github.com/orgs/test_org': cls.org_payload,
                'https://api.github.com/orgs/test_org/repos':
                cls.repos_payload,
            }

            def get_payload(url, *args, **kwargs):
                mock_response = Mock()
                if url in route_payload:
                    mock_response.json.return_value = route_payload[url]
                else:
                    mock_response.raise_for_status.side_effect = Exception(
                        'Not Found')
                return mock_response

            cls.get_patcher = patch("requests.get", side_effect=get_payload)
            cls.get_patcher.start()

        @ classmethod
        def tearDownClass(cls) -> None:
            """Tear down the class by stopping the patcher."""
            cls.get_patcher.stop()

        def test_public_repos(self) -> None:
            """Test for public repos."""
            client = GithubOrgClient("test_org")
            self.assertEqual(client.public_repos(), self.expected_repos)

        def test_public_repos_with_license(self) -> None:
            """Test for public repos with Apache 2.0 license filter."""
            client = GithubOrgClient("test_org")
            self.assertEqual(client.public_repos(
                license="apache-2.0"), self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
