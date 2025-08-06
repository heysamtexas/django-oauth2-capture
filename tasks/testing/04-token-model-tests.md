# Token Model Testing Implementation

## Objective
Create comprehensive test coverage for the `OAuthToken` model including field validation, properties, methods, database constraints, and model relationships. Currently, there are no dedicated tests for the model layer.

## Context
The `OAuthToken` model in `oauth2_capture/models.py` is the core data structure that stores OAuth tokens and user information. It includes:

**Key Fields:**
- `provider`, `user_id` (unique together constraint)
- `access_token`, `refresh_token` (sensitive data)
- `expires_at`, `refresh_token_expires_at` (datetime fields)
- `token_type`, `scope` (OAuth metadata)
- `owner` (ForeignKey to User)
- `profile_json` (JSONField for user data)
- `name` (derived from profile data)

**Key Properties:**
- `is_expired` (lines 71-75): Checks token expiration
- `expires_in_humanized` (lines 78-83): Human-readable expiration
- `username` (lines 86-88): Extracts username from profile_json

**Database Constraints:**
- Unique together on (`provider`, `user_id`)
- Foreign key relationship to Django User model

## Technical Details

### Test Categories
1. **Field Validation Tests**: Test field types, constraints, and validation
2. **Property Tests**: Test computed properties and their edge cases
3. **Constraint Tests**: Test unique constraints and foreign key relationships
4. **JSON Field Tests**: Test profile_json storage and retrieval
5. **Model Method Tests**: Test custom model methods
6. **Manager Tests**: Test custom querysets and model managers
7. **Migration Tests**: Test database schema changes

### Testing Areas
- **Data Integrity**: Ensure fields store and retrieve correctly
- **Validation**: Test field validation and error handling
- **Relationships**: Test foreign key relationships and cascading
- **Edge Cases**: Test null values, empty strings, edge cases
- **Performance**: Test query efficiency and indexing

## Testing Requirements
1. **Basic CRUD Tests**: Create, read, update, delete operations
2. **Field Validation Tests**: Test each field's validation rules
3. **Constraint Tests**: Test unique constraints and violations
4. **Property Tests**: Test computed properties with various data
5. **JSON Field Tests**: Test complex JSON data handling
6. **Relationship Tests**: Test User model relationships
7. **Query Tests**: Test common query patterns
8. **Edge Case Tests**: Test boundary conditions and error cases

## Dependencies
- Django test framework and database setup
- Test data fixtures for consistent testing
- Mock data for realistic JSON profiles

## Estimated Complexity
Simple (half day)

## Files to Create
- `oauth2_capture/tests/test_models.py`: Comprehensive model tests
- `oauth2_capture/tests/fixtures/profile_data.py`: Realistic profile JSON fixtures
- `oauth2_capture/tests/test_model_managers.py`: Custom manager tests (if any added)

## Example Code

### Model Test Base and Fixtures
```python
# oauth2_capture/tests/fixtures/profile_data.py
"""Realistic profile JSON data for testing."""

class ProfileDataFixtures:
    """Profile data fixtures for different providers."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    TWITTER_PROFILE = {
        "id": "123456789",
        "name": "Test User",
        "username": "testuser",
        "profile_image_url": "https://pbs.twimg.com/profile_images/123/avatar.jpg",
        "description": "Test user description",
        "verified": False,
        "followers_count": 100,
        "following_count": 50
    }
<<<<<<< HEAD
    
    GITHUB_PROFILE = {
        "login": "testuser",
        "id": 123456,
        "node_id": "MDQ6VXNlcjEyMzQ1Ng==", 
=======

    GITHUB_PROFILE = {
        "login": "testuser",
        "id": 123456,
        "node_id": "MDQ6VXNlcjEyMzQ1Ng==",
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
        "name": "Test User",
        "company": "Test Company",
        "blog": "https://testuser.github.io",
        "location": "San Francisco, CA",
        "email": "test@example.com",
        "bio": "Software developer",
        "public_repos": 25,
        "followers": 10,
        "following": 15
    }
<<<<<<< HEAD
    
    LINKEDIN_PROFILE = {
        "sub": "xyz123abc",
        "name": "Test User",
        "given_name": "Test", 
=======

    LINKEDIN_PROFILE = {
        "sub": "xyz123abc",
        "name": "Test User",
        "given_name": "Test",
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        "family_name": "User",
        "picture": "https://media.licdn.com/media/profile.jpg",
        "email": "test@example.com",
        "email_verified": True,
        "locale": "en-US"
    }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    # Edge case profiles for testing
    MINIMAL_PROFILE = {
        "id": "minimal_id"
    }
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    NULL_NAME_PROFILE = {
        "id": "null_name_id",
        "login": "nullnameuser",
        "name": None
    }
<<<<<<< HEAD
    
    EMPTY_PROFILE = {}
    
=======

    EMPTY_PROFILE = {}

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    COMPLEX_NESTED_PROFILE = {
        "id": "complex_id",
        "name": "Complex User",
        "username": "complexuser",
        "nested": {
            "deep": {
                "data": "value"
            }
        },
        "array_data": [1, 2, 3],
        "boolean_field": True,
        "null_field": None
    }
```

### Comprehensive Model Tests
```python
# oauth2_capture/tests/test_models.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from datetime import timedelta
import json

from oauth2_capture.models import OAuthToken
from .fixtures.profile_data import ProfileDataFixtures

class OAuthTokenModelTests(TestCase):
    """Test cases for OAuthToken model."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
<<<<<<< HEAD
            email='test2@example.com', 
            password='testpass123'
        )
    
=======
            email='test2@example.com',
            password='testpass123'
        )

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def create_token(self, **kwargs):
        """Helper to create test tokens with defaults."""
        defaults = {
            'provider': 'twitter',
            'user_id': '123456',
            'access_token': 'test_access_token',
            'refresh_token': 'test_refresh_token',
            'token_type': 'Bearer',
            'scope': 'read write',
            'owner': self.user,
            'name': 'Test User',
            'profile_json': ProfileDataFixtures.TWITTER_PROFILE
        }
        defaults.update(kwargs)
        return OAuthToken.objects.create(**defaults)
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_token_creation_with_required_fields(self):
        """Test creating token with minimum required fields."""
        token = OAuthToken.objects.create(
            provider='github',
            user_id='987654',
            access_token='github_access_token',
            owner=self.user
        )
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        self.assertEqual(token.provider, 'github')
        self.assertEqual(token.user_id, '987654')
        self.assertEqual(token.access_token, 'github_access_token')
        self.assertEqual(token.owner, self.user)
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Optional fields should have defaults
        self.assertEqual(token.refresh_token, '')
        self.assertEqual(token.token_type, '')
        self.assertEqual(token.scope, '')
        self.assertEqual(token.name, '')
<<<<<<< HEAD
        
    def test_token_string_representation(self):
        """Test the __str__ method of OAuthToken."""
        token = self.create_token()
        
        expected = f"twitter (Test User) @ {self.user}"
        self.assertEqual(str(token), expected)
        
    def test_token_string_representation_no_name(self):
        """Test __str__ method when name is empty."""
        token = self.create_token(name='')
        
        expected = f"twitter () @ {self.user}"
        self.assertEqual(str(token), expected)
    
=======

    def test_token_string_representation(self):
        """Test the __str__ method of OAuthToken."""
        token = self.create_token()

        expected = f"twitter (Test User) @ {self.user}"
        self.assertEqual(str(token), expected)

    def test_token_string_representation_no_name(self):
        """Test __str__ method when name is empty."""
        token = self.create_token(name='')

        expected = f"twitter () @ {self.user}"
        self.assertEqual(str(token), expected)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_unique_constraint_provider_user_id(self):
        """Test unique constraint on provider + user_id combination."""
        # Create first token
        self.create_token()
<<<<<<< HEAD
        
        # Attempting to create second token with same provider + user_id should fail
        with self.assertRaises(IntegrityError):
            self.create_token()
    
=======

        # Attempting to create second token with same provider + user_id should fail
        with self.assertRaises(IntegrityError):
            self.create_token()

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_unique_constraint_allows_different_providers(self):
        """Test that same user_id is allowed for different providers."""
        token1 = self.create_token(provider='twitter')
        token2 = self.create_token(provider='github', user_id='123456')  # Same user_id, different provider
<<<<<<< HEAD
        
        self.assertNotEqual(token1.id, token2.id)
        self.assertEqual(token1.user_id, token2.user_id)
        self.assertNotEqual(token1.provider, token2.provider)
    
=======

        self.assertNotEqual(token1.id, token2.id)
        self.assertEqual(token1.user_id, token2.user_id)
        self.assertNotEqual(token1.provider, token2.provider)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_unique_constraint_allows_different_user_ids(self):
        """Test that different user_ids are allowed for same provider."""
        token1 = self.create_token(user_id='123456')
        token2 = self.create_token(user_id='654321')  # Different user_id, same provider
<<<<<<< HEAD
        
        self.assertNotEqual(token1.id, token2.id)
        self.assertNotEqual(token1.user_id, token2.user_id)
        self.assertEqual(token1.provider, token2.provider)
    
=======

        self.assertNotEqual(token1.id, token2.id)
        self.assertNotEqual(token1.user_id, token2.user_id)
        self.assertEqual(token1.provider, token2.provider)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_foreign_key_cascade_delete(self):
        """Test that tokens are deleted when user is deleted."""
        token = self.create_token()
        token_id = token.id
<<<<<<< HEAD
        
        # Verify token exists
        self.assertTrue(OAuthToken.objects.filter(id=token_id).exists())
        
        # Delete the user
        self.user.delete()
        
        # Token should be deleted due to CASCADE
        self.assertFalse(OAuthToken.objects.filter(id=token_id).exists())
    
=======

        # Verify token exists
        self.assertTrue(OAuthToken.objects.filter(id=token_id).exists())

        # Delete the user
        self.user.delete()

        # Token should be deleted due to CASCADE
        self.assertFalse(OAuthToken.objects.filter(id=token_id).exists())

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_related_name_oauth_tokens(self):
        """Test the related_name for accessing tokens from user."""
        token1 = self.create_token(provider='twitter')
        token2 = self.create_token(provider='github', user_id='different_id')
<<<<<<< HEAD
        
        # Should be able to access tokens via related name
        user_tokens = self.user.oauth_tokens.all()
        
        self.assertEqual(len(user_tokens), 2)
        self.assertIn(token1, user_tokens)
        self.assertIn(token2, user_tokens)
    
=======

        # Should be able to access tokens via related name
        user_tokens = self.user.oauth_tokens.all()

        self.assertEqual(len(user_tokens), 2)
        self.assertIn(token1, user_tokens)
        self.assertIn(token2, user_tokens)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_is_expired_property_with_future_date(self):
        """Test is_expired property when token expires in the future."""
        future_time = timezone.now() + timedelta(hours=1)
        token = self.create_token(expires_at=future_time)
<<<<<<< HEAD
        
        self.assertFalse(token.is_expired)
    
=======

        self.assertFalse(token.is_expired)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_is_expired_property_with_past_date(self):
        """Test is_expired property when token has expired."""
        past_time = timezone.now() - timedelta(hours=1)
        token = self.create_token(expires_at=past_time)
<<<<<<< HEAD
        
        self.assertTrue(token.is_expired)
    
    def test_is_expired_property_with_no_expiration(self):
        """Test is_expired property when expires_at is None."""
        token = self.create_token(expires_at=None)
        
        self.assertFalse(token.is_expired)  # No expiration means never expired
    
=======

        self.assertTrue(token.is_expired)

    def test_is_expired_property_with_no_expiration(self):
        """Test is_expired property when expires_at is None."""
        token = self.create_token(expires_at=None)

        self.assertFalse(token.is_expired)  # No expiration means never expired

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_expires_in_humanized_future_date(self):
        """Test expires_in_humanized for future expiration."""
        future_time = timezone.now() + timedelta(hours=2)
        token = self.create_token(expires_at=future_time)
<<<<<<< HEAD
        
        humanized = token.expires_in_humanized
        
        # Should contain time reference (exact format may vary by Django version)
        self.assertIsInstance(humanized, str)
        self.assertNotEqual(humanized, "Never")
    
    def test_expires_in_humanized_past_date(self):
        """Test expires_in_humanized for past expiration.""" 
        past_time = timezone.now() - timedelta(hours=2)
        token = self.create_token(expires_at=past_time)
        
        humanized = token.expires_in_humanized
        
        # Should indicate past time
        self.assertIsInstance(humanized, str)
        self.assertNotEqual(humanized, "Never")
    
    def test_expires_in_humanized_no_expiration(self):
        """Test expires_in_humanized when expires_at is None."""
        token = self.create_token(expires_at=None)
        
        self.assertEqual(token.expires_in_humanized, "Never")
    
=======

        humanized = token.expires_in_humanized

        # Should contain time reference (exact format may vary by Django version)
        self.assertIsInstance(humanized, str)
        self.assertNotEqual(humanized, "Never")

    def test_expires_in_humanized_past_date(self):
        """Test expires_in_humanized for past expiration."""
        past_time = timezone.now() - timedelta(hours=2)
        token = self.create_token(expires_at=past_time)

        humanized = token.expires_in_humanized

        # Should indicate past time
        self.assertIsInstance(humanized, str)
        self.assertNotEqual(humanized, "Never")

    def test_expires_in_humanized_no_expiration(self):
        """Test expires_in_humanized when expires_at is None."""
        token = self.create_token(expires_at=None)

        self.assertEqual(token.expires_in_humanized, "Never")

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_username_property_with_username_field(self):
        """Test username property extracts from profile_json username field."""
        profile = ProfileDataFixtures.TWITTER_PROFILE.copy()
        token = self.create_token(profile_json=profile)
<<<<<<< HEAD
        
        self.assertEqual(token.username, "testuser")
    
=======

        self.assertEqual(token.username, "testuser")

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_username_property_with_login_field(self):
        """Test username property falls back to login field."""
        profile = ProfileDataFixtures.GITHUB_PROFILE.copy()
        del profile['username']  # Remove username field if it exists
        token = self.create_token(profile_json=profile)
<<<<<<< HEAD
        
        self.assertEqual(token.username, "testuser")  # Should use login field
    
=======

        self.assertEqual(token.username, "testuser")  # Should use login field

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_username_property_fallback_to_name(self):
        """Test username property falls back to name field."""
        token = self.create_token(
            profile_json={'id': '123', 'name': 'Fallback Name'},
            name='Fallback Name'
        )
<<<<<<< HEAD
        
        self.assertEqual(token.username, "Fallback Name")
    
=======

        self.assertEqual(token.username, "Fallback Name")

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_username_property_with_null_values(self):
        """Test username property handles null and empty values."""
        profile = ProfileDataFixtures.NULL_NAME_PROFILE.copy()
        token = self.create_token(profile_json=profile, name='')
<<<<<<< HEAD
        
        # Should fallback to login when name is null
        self.assertEqual(token.username, "nullnameuser")
    
    def test_username_property_empty_profile(self):
        """Test username property with minimal profile data."""
        token = self.create_token(profile_json={}, name='Model Name')
        
        # Should fall back to model name field
        self.assertEqual(token.username, "Model Name")
    
=======

        # Should fallback to login when name is null
        self.assertEqual(token.username, "nullnameuser")

    def test_username_property_empty_profile(self):
        """Test username property with minimal profile data."""
        token = self.create_token(profile_json={}, name='Model Name')

        # Should fall back to model name field
        self.assertEqual(token.username, "Model Name")

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_json_field_storage_and_retrieval(self):
        """Test JSONField properly stores and retrieves complex data."""
        complex_profile = ProfileDataFixtures.COMPLEX_NESTED_PROFILE
        token = self.create_token(profile_json=complex_profile)
<<<<<<< HEAD
        
        # Refresh from database
        token.refresh_from_db()
        
=======

        # Refresh from database
        token.refresh_from_db()

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Should preserve complex data structure
        self.assertEqual(token.profile_json['nested']['deep']['data'], 'value')
        self.assertEqual(token.profile_json['array_data'], [1, 2, 3])
        self.assertTrue(token.profile_json['boolean_field'])
        self.assertIsNone(token.profile_json['null_field'])
<<<<<<< HEAD
    
    def test_json_field_null_value(self):
        """Test JSONField handles null values properly."""
        token = self.create_token(profile_json=None)
        
        self.assertIsNone(token.profile_json)
        
        # username property should handle null profile_json
        self.assertEqual(token.username, "Test User")  # Falls back to name field
    
=======

    def test_json_field_null_value(self):
        """Test JSONField handles null values properly."""
        token = self.create_token(profile_json=None)

        self.assertIsNone(token.profile_json)

        # username property should handle null profile_json
        self.assertEqual(token.username, "Test User")  # Falls back to name field

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_field_max_lengths(self):
        """Test field max lengths where applicable."""
        # Test provider field (max_length=50)
        long_provider = 'x' * 51  # 51 characters
        with self.assertRaises(ValidationError):
            token = OAuthToken(
                provider=long_provider,
                user_id='123',
                access_token='token',
                owner=self.user
            )
            token.full_clean()
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Test name field (max_length=100)
        long_name = 'x' * 101  # 101 characters
        with self.assertRaises(ValidationError):
            token = OAuthToken(
                provider='twitter',
                user_id='123',
                access_token='token',
                owner=self.user,
                name=long_name
            )
            token.full_clean()
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_refresh_token_field_length(self):
        """Test refresh_token field can handle expected token lengths."""
        # Test with 500 character token (should work)
        long_token = 'x' * 500
        token = self.create_token(refresh_token=long_token)
<<<<<<< HEAD
        
        self.assertEqual(len(token.refresh_token), 500)
        
=======

        self.assertEqual(len(token.refresh_token), 500)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Test with 501 character token (should fail validation)
        very_long_token = 'x' * 501
        with self.assertRaises(ValidationError):
            token = OAuthToken(
                provider='twitter',
                user_id='123',
<<<<<<< HEAD
                access_token='token', 
=======
                access_token='token',
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
                refresh_token=very_long_token,
                owner=self.user
            )
            token.full_clean()
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_model_verbose_names(self):
        """Test model meta verbose names."""
        self.assertEqual(OAuthToken._meta.verbose_name, "OAuth Token")
        self.assertEqual(OAuthToken._meta.verbose_name_plural, "OAuth Tokens")
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_created_at_auto_now_add(self):
        """Test that created_at is automatically set on creation."""
        before_creation = timezone.now()
        token = self.create_token()
        after_creation = timezone.now()
<<<<<<< HEAD
        
        self.assertIsNotNone(token.created_at)
        self.assertGreaterEqual(token.created_at, before_creation)
        self.assertLessEqual(token.created_at, after_creation)
        
=======

        self.assertIsNotNone(token.created_at)
        self.assertGreaterEqual(token.created_at, before_creation)
        self.assertLessEqual(token.created_at, after_creation)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Verify it doesn't change on update
        original_created_at = token.created_at
        token.name = "Updated Name"
        token.save()
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        self.assertEqual(token.created_at, original_created_at)

class OAuthTokenQueryTests(TestCase):
    """Test cases for common OAuthToken queries."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        self.user2 = User.objects.create_user(
<<<<<<< HEAD
            username='testuser2', 
            email='test2@example.com',
            password='testpass'
        )
    
=======
            username='testuser2',
            email='test2@example.com',
            password='testpass'
        )

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_filter_by_provider(self):
        """Test filtering tokens by provider."""
        twitter_token = OAuthToken.objects.create(
            provider='twitter',
            user_id='123',
            access_token='twitter_token',
            owner=self.user
        )
        github_token = OAuthToken.objects.create(
            provider='github',
            user_id='456',
            access_token='github_token',
            owner=self.user
        )
<<<<<<< HEAD
        
        twitter_tokens = OAuthToken.objects.filter(provider='twitter')
        github_tokens = OAuthToken.objects.filter(provider='github')
        
=======

        twitter_tokens = OAuthToken.objects.filter(provider='twitter')
        github_tokens = OAuthToken.objects.filter(provider='github')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        self.assertIn(twitter_token, twitter_tokens)
        self.assertNotIn(github_token, twitter_tokens)
        self.assertIn(github_token, github_tokens)
        self.assertNotIn(twitter_token, github_tokens)
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_filter_by_owner(self):
        """Test filtering tokens by owner."""
        user1_token = OAuthToken.objects.create(
            provider='twitter',
            user_id='123',
            access_token='user1_token',
            owner=self.user
        )
        user2_token = OAuthToken.objects.create(
            provider='twitter',
            user_id='456',
            access_token='user2_token',
            owner=self.user2
        )
<<<<<<< HEAD
        
        user1_tokens = OAuthToken.objects.filter(owner=self.user)
        user2_tokens = OAuthToken.objects.filter(owner=self.user2)
        
=======

        user1_tokens = OAuthToken.objects.filter(owner=self.user)
        user2_tokens = OAuthToken.objects.filter(owner=self.user2)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        self.assertIn(user1_token, user1_tokens)
        self.assertNotIn(user2_token, user1_tokens)
        self.assertIn(user2_token, user2_tokens)
        self.assertNotIn(user1_token, user2_tokens)
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_filter_expired_tokens(self):
        """Test filtering expired vs non-expired tokens."""
        expired_token = OAuthToken.objects.create(
            provider='twitter',
            user_id='123',
            access_token='expired_token',
            expires_at=timezone.now() - timedelta(hours=1),
            owner=self.user
        )
        valid_token = OAuthToken.objects.create(
<<<<<<< HEAD
            provider='github', 
=======
            provider='github',
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            user_id='456',
            access_token='valid_token',
            expires_at=timezone.now() + timedelta(hours=1),
            owner=self.user
        )
        never_expires_token = OAuthToken.objects.create(
            provider='linkedin',
            user_id='789',
            access_token='never_expires',
            expires_at=None,
            owner=self.user
        )
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Filter expired tokens
        expired_tokens = OAuthToken.objects.filter(expires_at__lt=timezone.now())
        self.assertIn(expired_token, expired_tokens)
        self.assertNotIn(valid_token, expired_tokens)
        self.assertNotIn(never_expires_token, expired_tokens)
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Filter valid tokens (not expired)
        valid_tokens = OAuthToken.objects.filter(
            models.Q(expires_at__gt=timezone.now()) | models.Q(expires_at__isnull=True)
        )
        self.assertNotIn(expired_token, valid_tokens)
        self.assertIn(valid_token, valid_tokens)
        self.assertIn(never_expires_token, valid_tokens)
```

## Success Criteria
- [ ] Complete test coverage for all model fields and properties
- [ ] Database constraint testing (unique constraints, foreign keys)
- [ ] JSON field functionality testing with complex data
- [ ] Property method testing with edge cases
- [ ] Field validation testing including max lengths
- [ ] Query pattern testing for common use cases
- [ ] Model method testing for custom functionality
- [ ] Edge case handling (null values, empty data, etc.)
<<<<<<< HEAD
- [ ] Performance considerations for common queries
=======
- [ ] Performance considerations for common queries
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
