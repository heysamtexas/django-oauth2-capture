from django.test import TestCase
from unittest.mock import Mock, patch
import requests
import time

from oauth2_capture.services.oauth2 import retry_with_backoff


class RetryWithBackoffTests(TestCase):
    @patch("time.sleep")
    def test_successful_first_attempt(self, mock_sleep):
        # Test when the first request attempt succeeds
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200

        mock_request_func = Mock(return_value=mock_response)

        result = retry_with_backoff(mock_request_func)

        mock_request_func.assert_called_once()
        mock_sleep.assert_not_called()
        self.assertEqual(result, mock_response)

    @patch("time.sleep")
    def test_retry_with_429_then_success(self, mock_sleep):
        # Test when first attempt gets 429, then succeeds
        mock_response_429 = Mock(spec=requests.Response)
        mock_response_429.status_code = 429
        mock_response_429.headers = {}

        mock_response_200 = Mock(spec=requests.Response)
        mock_response_200.status_code = 200

        mock_request_func = Mock(side_effect=[mock_response_429, mock_response_200])

        result = retry_with_backoff(mock_request_func)

        self.assertEqual(mock_request_func.call_count, 2)
        mock_sleep.assert_called_once_with(5)  # First fallback delay
        self.assertEqual(result, mock_response_200)

    @patch("time.sleep")
    def test_retry_with_retry_after_header(self, mock_sleep):
        # Test when response has Retry-After header
        mock_response_429 = Mock(spec=requests.Response)
        mock_response_429.status_code = 429
        mock_response_429.headers = {"Retry-After": "15"}

        mock_response_200 = Mock(spec=requests.Response)
        mock_response_200.status_code = 200

        mock_request_func = Mock(side_effect=[mock_response_429, mock_response_200])

        result = retry_with_backoff(mock_request_func)

        self.assertEqual(mock_request_func.call_count, 2)
        mock_sleep.assert_called_once_with(15)  # Should use Retry-After value
        self.assertEqual(result, mock_response_200)

    @patch("time.sleep")
    def test_invalid_retry_after_header(self, mock_sleep):
        # Test when Retry-After header is invalid
        mock_response_429 = Mock(spec=requests.Response)
        mock_response_429.status_code = 429
        mock_response_429.headers = {"Retry-After": "not-a-number"}

        mock_response_200 = Mock(spec=requests.Response)
        mock_response_200.status_code = 200

        mock_request_func = Mock(side_effect=[mock_response_429, mock_response_200])

        result = retry_with_backoff(mock_request_func)

        self.assertEqual(mock_request_func.call_count, 2)
        mock_sleep.assert_called_once_with(5)  # Should use fallback delay
        self.assertEqual(result, mock_response_200)

    @patch("time.sleep")
    def test_multiple_retries_with_fallback_delays(self, mock_sleep):
        # Test with multiple retries using fallback delays
        mock_response_429 = Mock(spec=requests.Response)
        mock_response_429.status_code = 429
        mock_response_429.headers = {}

        mock_response_200 = Mock(spec=requests.Response)
        mock_response_200.status_code = 200

        mock_request_func = Mock(side_effect=[
            mock_response_429,
            mock_response_429,
            mock_response_429,
            mock_response_200
        ])

        result = retry_with_backoff(mock_request_func)

        self.assertEqual(mock_request_func.call_count, 4)
        # Check that sleep was called with the correct fallback delays
        mock_sleep.assert_any_call(5)   # First retry
        mock_sleep.assert_any_call(10)  # Second retry
        mock_sleep.assert_any_call(20)  # Third retry
        self.assertEqual(result, mock_response_200)

    @patch("time.sleep")
    def test_max_retries_exceeded(self, mock_sleep):
        # Test when max retries is exceeded
        mock_response_429 = Mock(spec=requests.Response)
        mock_response_429.status_code = 429
        mock_response_429.headers = {}

        # All attempts return 429
        mock_request_func = Mock(return_value=mock_response_429)

        result = retry_with_backoff(mock_request_func, max_retries=3)

        self.assertEqual(mock_request_func.call_count, 3)
        # Should return the last response after max retries
        self.assertEqual(result, mock_response_429)

    @patch("time.sleep")
    def test_custom_fallback_delays(self, mock_sleep):
        # Test with custom fallback delays
        mock_response_429 = Mock(spec=requests.Response)
        mock_response_429.status_code = 429
        mock_response_429.headers = {}

        mock_response_200 = Mock(spec=requests.Response)
        mock_response_200.status_code = 200

        mock_request_func = Mock(side_effect=[mock_response_429, mock_response_200])

        custom_delays = (2, 4, 8)
        result = retry_with_backoff(mock_request_func, fallback_delays=custom_delays)

        self.assertEqual(mock_request_func.call_count, 2)
        mock_sleep.assert_called_once_with(2)  # First custom delay
        self.assertEqual(result, mock_response_200)

    @patch("time.sleep")
    def test_handle_index_out_of_bounds(self, mock_sleep):
        # Test when attempt index exceeds fallback_delays length
        mock_response_429 = Mock(spec=requests.Response)
        mock_response_429.status_code = 429
        mock_response_429.headers = {}

        mock_response_200 = Mock(spec=requests.Response)
        mock_response_200.status_code = 200

        mock_request_func = Mock(side_effect=[
            mock_response_429,
            mock_response_429,
            mock_response_429,
            mock_response_200
        ])

        # Only provide 2 fallback delays
        result = retry_with_backoff(
            mock_request_func,
            max_retries=4,
            fallback_delays=(3, 6)
        )

        self.assertEqual(mock_request_func.call_count, 4)
        # The third attempt should use the last fallback delay (6)
        mock_sleep.assert_any_call(3)  # First retry
        mock_sleep.assert_any_call(6)  # Second retry
        mock_sleep.assert_any_call(6)  # Third retry (uses last value)
        self.assertEqual(result, mock_response_200)
