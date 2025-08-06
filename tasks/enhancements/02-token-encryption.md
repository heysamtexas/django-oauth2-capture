# Token Encryption at Rest Implementation

## Objective
Implement encryption for OAuth tokens stored in the database to enhance security for production deployments. This addresses the security concern of storing sensitive access tokens and refresh tokens in plain text.

## Context
Currently, OAuth tokens are stored in plain text in the database:

**Security Concerns:**
- Access tokens stored as plain text in `access_token` field (TextField)
- Refresh tokens stored as plain text in `refresh_token` field (CharField)
- Database backups contain sensitive tokens in readable format
- Database administrators have access to all tokens
- Potential data breach impact includes immediate token misuse

**Production Requirements:**
- Tokens should be encrypted at rest
- Encryption should be transparent to application code
- Key management should be secure and configurable
- Performance impact should be minimal
- Existing tokens should be migrated seamlessly

**Compliance Considerations:**
- Many security frameworks require encryption of sensitive data
- GDPR and similar privacy regulations may require additional protection
- Industry best practices recommend encryption of authentication credentials

## Technical Details

### Encryption Strategy

1. **Field-Level Encryption**: Encrypt individual token fields
2. **Symmetric Encryption**: Use AES encryption for performance
3. **Key Derivation**: Use Django's SECRET_KEY or dedicated encryption key
4. **Transparent Operation**: Application code remains unchanged
5. **Migration Support**: Gradual migration of existing tokens

### Implementation Approach

1. **Custom Model Fields**: Create encrypted field types
2. **Key Management**: Secure key storage and rotation
3. **Database Migration**: Migrate existing plain text tokens
4. **Configuration**: Optional encryption with fallback
5. **Performance**: Minimal overhead for encryption/decryption

### Encryption Algorithm

- **Algorithm**: AES-256-GCM (authenticated encryption)
- **Key Derivation**: PBKDF2 or HKDF from SECRET_KEY
- **IV/Nonce**: Unique for each token, stored with ciphertext
- **Authentication**: Built-in with GCM mode

## Testing Requirements
1. **Encryption/Decryption Tests**: Verify round-trip encryption
2. **Migration Tests**: Test conversion of existing tokens
3. **Performance Tests**: Measure encryption overhead
4. **Key Rotation Tests**: Verify key rotation functionality
5. **Backward Compatibility Tests**: Ensure existing code works
6. **Security Tests**: Verify encrypted tokens are unreadable

## Dependencies
- Cryptographic library (e.g., `cryptography` package)
- Django migration system for data migration
- Optional: dedicated key management system
- Database backup/restore considerations

## Estimated Complexity
Medium (1 day)

## Files to Create/Modify
- `oauth2_capture/fields.py`: Create encrypted field classes
- `oauth2_capture/encryption.py`: Encryption utilities and key management
- `oauth2_capture/models.py`: Update OAuthToken model to use encrypted fields
- `oauth2_capture/migrations/`: Create migration for existing tokens
- `oauth2_capture/management/commands/`: Key rotation and migration commands
- `oauth2_capture/tests/test_encryption.py`: Comprehensive encryption tests
- `docs/security.md`: Documentation for encryption configuration

## Example Implementation

### Encryption Utilities
```python
# oauth2_capture/encryption.py
import os
import base64
from typing import Optional, Union
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class TokenEncryption:
    """Token encryption and decryption utilities."""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def __init__(self, key: Optional[bytes] = None):
        """Initialize with encryption key."""
        self.key = key or self._derive_key()
        self.fernet = Fernet(self.key)
<<<<<<< HEAD
    
    def _derive_key(self) -> bytes:
        """Derive encryption key from Django SECRET_KEY or dedicated key."""
        
=======

    def _derive_key(self) -> bytes:
        """Derive encryption key from Django SECRET_KEY or dedicated key."""

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Check for dedicated encryption key first
        encryption_key = getattr(settings, 'OAUTH2_ENCRYPTION_KEY', None)
        if encryption_key:
            if isinstance(encryption_key, str):
                return base64.urlsafe_b64encode(encryption_key.encode()[:32].ljust(32, b'\0'))
            return encryption_key
<<<<<<< HEAD
        
        # Fall back to deriving from SECRET_KEY
        secret_key = settings.SECRET_KEY.encode()
        
        # Use a fixed salt for consistency (in production, consider configurable salt)
        salt = b'oauth2_token_salt_v1'  
        
=======

        # Fall back to deriving from SECRET_KEY
        secret_key = settings.SECRET_KEY.encode()

        # Use a fixed salt for consistency (in production, consider configurable salt)
        salt = b'oauth2_token_salt_v1'

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
<<<<<<< HEAD
        
        key = base64.urlsafe_b64encode(kdf.derive(secret_key))
        return key
    
=======

        key = base64.urlsafe_b64encode(kdf.derive(secret_key))
        return key

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def encrypt(self, plaintext: str) -> str:
        """Encrypt a plaintext string."""
        if not plaintext:
            return plaintext
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        try:
            encrypted_bytes = self.fernet.encrypt(plaintext.encode('utf-8'))
            return base64.urlsafe_b64encode(encrypted_bytes).decode('ascii')
        except Exception as e:
            logger.error("Token encryption failed: %s", str(e))
            raise
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def decrypt(self, ciphertext: str) -> str:
        """Decrypt a ciphertext string."""
        if not ciphertext:
            return ciphertext
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        try:
            encrypted_bytes = base64.urlsafe_b64decode(ciphertext.encode('ascii'))
            decrypted_bytes = self.fernet.decrypt(encrypted_bytes)
            return decrypted_bytes.decode('utf-8')
        except Exception as e:
            logger.error("Token decryption failed: %s", str(e))
            # In production, consider whether to raise or return empty string
            raise
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def is_encrypted(self, value: str) -> bool:
        """Check if a value appears to be encrypted."""
        if not value:
            return False
<<<<<<< HEAD
        
        try:
            # Try to decode as base64 - encrypted values should be base64 encoded
            base64.urlsafe_b64decode(value.encode('ascii'))
            
            # Additional heuristic: encrypted values have specific length patterns
            # Fernet tokens are always 145+ characters when base64 encoded
            return len(value) >= 100  # Conservative estimate
            
=======

        try:
            # Try to decode as base64 - encrypted values should be base64 encoded
            base64.urlsafe_b64decode(value.encode('ascii'))

            # Additional heuristic: encrypted values have specific length patterns
            # Fernet tokens are always 145+ characters when base64 encoded
            return len(value) >= 100  # Conservative estimate

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        except Exception:
            return False

# Global encryption instance
_encryption_instance = None

def get_encryption() -> TokenEncryption:
    """Get the global encryption instance."""
    global _encryption_instance
    if _encryption_instance is None:
        _encryption_instance = TokenEncryption()
    return _encryption_instance

def encrypt_token(token: str) -> str:
    """Convenience function to encrypt a token."""
    return get_encryption().encrypt(token)

def decrypt_token(encrypted_token: str) -> str:
    """Convenience function to decrypt a token."""
    return get_encryption().decrypt(encrypted_token)

def is_token_encrypted(token: str) -> bool:
    """Check if a token is encrypted."""
    return get_encryption().is_encrypted(token)
```

### Encrypted Model Fields
```python
# oauth2_capture/fields.py
from django.db import models
from django.core.exceptions import ValidationError
from .encryption import encrypt_token, decrypt_token, is_token_encrypted
import logging

logger = logging.getLogger(__name__)

class EncryptedTextField(models.TextField):
    """TextField that automatically encrypts/decrypts values."""
<<<<<<< HEAD
    
    description = "Encrypted text field"
    
=======

    description = "Encrypted text field"

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def __init__(self, *args, **kwargs):
        # Remove encryption-specific kwargs
        self.encrypt_enabled = kwargs.pop('encrypt_enabled', True)
        self.migration_mode = kwargs.pop('migration_mode', False)
        super().__init__(*args, **kwargs)
<<<<<<< HEAD
    
    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        
        # Set up descriptor for transparent encryption/decryption
        setattr(cls, self.name, EncryptedFieldDescriptor(self))
    
=======

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)

        # Set up descriptor for transparent encryption/decryption
        setattr(cls, self.name, EncryptedFieldDescriptor(self))

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def from_db_value(self, value, expression, connection):
        """Convert database value to Python value."""
        if value is None:
            return value
<<<<<<< HEAD
        
        # During migration, some values might not be encrypted yet
        if self.migration_mode or not self.encrypt_enabled:
            return value
        
=======

        # During migration, some values might not be encrypted yet
        if self.migration_mode or not self.encrypt_enabled:
            return value

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        try:
            # Only decrypt if the value appears to be encrypted
            if is_token_encrypted(value):
                return decrypt_token(value)
            else:
                # Handle legacy unencrypted values during migration
                logger.debug("Found unencrypted token during read - migration may be needed")
                return value
        except Exception as e:
            logger.error("Failed to decrypt token: %s", str(e))
            # Return empty string rather than failing completely
            return ""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def to_python(self, value):
        """Convert any value to Python representation."""
        if value is None:
            return value
        return str(value)
<<<<<<< HEAD
    
    def get_prep_value(self, value):
        """Convert Python value for database storage.""" 
        if value is None or value == "":
            return value
        
        if not self.encrypt_enabled:
            return value
        
=======

    def get_prep_value(self, value):
        """Convert Python value for database storage."""
        if value is None or value == "":
            return value

        if not self.encrypt_enabled:
            return value

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        try:
            # Only encrypt if not already encrypted
            if not is_token_encrypted(value):
                return encrypt_token(str(value))
            return value
        except Exception as e:
            logger.error("Failed to encrypt token: %s", str(e))
            raise ValidationError(f"Token encryption failed: {str(e)}")

class EncryptedCharField(models.CharField):
    """CharField that automatically encrypts/decrypts values."""
<<<<<<< HEAD
    
    description = "Encrypted char field"
    
    def __init__(self, *args, **kwargs):
        self.encrypt_enabled = kwargs.pop('encrypt_enabled', True)
        self.migration_mode = kwargs.pop('migration_mode', False)
        
=======

    description = "Encrypted char field"

    def __init__(self, *args, **kwargs):
        self.encrypt_enabled = kwargs.pop('encrypt_enabled', True)
        self.migration_mode = kwargs.pop('migration_mode', False)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Encrypted values are longer - adjust max_length if needed
        original_max_length = kwargs.get('max_length', 500)
        if self.encrypt_enabled and original_max_length < 200:
            kwargs['max_length'] = max(original_max_length * 3, 500)
<<<<<<< HEAD
        
        super().__init__(*args, **kwargs)
    
    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, EncryptedFieldDescriptor(self))
    
=======

        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, self.name, EncryptedFieldDescriptor(self))

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def from_db_value(self, value, expression, connection):
        """Convert database value to Python value."""
        if value is None:
            return value
<<<<<<< HEAD
        
        if self.migration_mode or not self.encrypt_enabled:
            return value
        
=======

        if self.migration_mode or not self.encrypt_enabled:
            return value

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        try:
            if is_token_encrypted(value):
                return decrypt_token(value)
            else:
                logger.debug("Found unencrypted token in CharField during read")
                return value
        except Exception as e:
            logger.error("Failed to decrypt CharField token: %s", str(e))
            return ""
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def get_prep_value(self, value):
        """Convert Python value for database storage."""
        if value is None or value == "":
            return value
<<<<<<< HEAD
        
        if not self.encrypt_enabled:
            return value
        
        try:
            if not is_token_encrypted(value):
                encrypted = encrypt_token(str(value))
                
                # Check if encrypted value fits in field length
                if len(encrypted) > self.max_length:
                    logger.warning(
                        "Encrypted token length (%d) exceeds field max_length (%d)", 
                        len(encrypted), self.max_length
                    )
                
=======

        if not self.encrypt_enabled:
            return value

        try:
            if not is_token_encrypted(value):
                encrypted = encrypt_token(str(value))

                # Check if encrypted value fits in field length
                if len(encrypted) > self.max_length:
                    logger.warning(
                        "Encrypted token length (%d) exceeds field max_length (%d)",
                        len(encrypted), self.max_length
                    )

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
                return encrypted
            return value
        except Exception as e:
            logger.error("Failed to encrypt CharField token: %s", str(e))
            raise ValidationError(f"Token encryption failed: {str(e)}")

class EncryptedFieldDescriptor:
    """Descriptor for encrypted fields to handle transparent encryption/decryption."""
<<<<<<< HEAD
    
    def __init__(self, field):
        self.field = field
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        # Get the raw value from the instance
        value = instance.__dict__.get(self.field.attname)
        
        if value is None:
            return None
        
=======

    def __init__(self, field):
        self.field = field

    def __get__(self, instance, owner):
        if instance is None:
            return self

        # Get the raw value from the instance
        value = instance.__dict__.get(self.field.attname)

        if value is None:
            return None

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Return decrypted value if encryption is enabled
        if self.field.encrypt_enabled and not self.field.migration_mode:
            try:
                if is_token_encrypted(value):
                    return decrypt_token(value)
            except Exception as e:
                logger.error("Field descriptor decryption failed: %s", str(e))
<<<<<<< HEAD
        
        return value
    
=======

        return value

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def __set__(self, instance, value):
        # Store the value as-is in the instance
        # Encryption happens in get_prep_value when saving to database
        instance.__dict__[self.field.attname] = value
```

### Updated Model with Encryption
```python
# Updated oauth2_capture/models.py
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.utils import timezone
from django.conf import settings
from shortuuid.django_fields import ShortUUIDField
from .fields import EncryptedTextField, EncryptedCharField

class OAuthToken(models.Model):
    """Model to capture the OAuth token for API access with encrypted storage."""

    provider = models.CharField(
        max_length=50,
        help_text="The name of the OAuth provider (e.g., 'google', 'github', 'facebook').",
    )
    slug = ShortUUIDField()
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    # Use encrypted fields for sensitive data
    access_token = EncryptedTextField(
        help_text="The OAuth access token for API access (encrypted at rest).",
        encrypt_enabled=getattr(settings, 'OAUTH2_ENCRYPT_TOKENS', True)
    )
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The exact expiration time of the access token.",
    )
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    refresh_token = EncryptedCharField(
        max_length=1500,  # Increased to handle encrypted values
        blank=True,
        default="",
        help_text="The refresh token, if provided by the OAuth provider (encrypted at rest).",
        encrypt_enabled=getattr(settings, 'OAUTH2_ENCRYPT_TOKENS', True)
    )
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    refresh_token_expires_at = models.DateTimeField(
        null=True, blank=True, help_text="The expiration time of the refresh token."
    )
    token_type = models.CharField(
        max_length=50,
        blank=True,
        default="",
        help_text="Type of the token, typically 'Bearer'.",
    )
    scope = models.TextField(
        blank=True,
        default="",
        help_text="Scopes granted by the OAuth provider (e.g., 'email profile').",
    )
    user_id = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="The unique ID of the user with the OAuth provider.",
    )
    owner = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="oauth_tokens",
        help_text="A reference to the local user this OAuth token is associated with.",
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="The timestamp when the token was issued.")

    profile_json = models.JSONField(null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        """Metaclass options for the model."""
        unique_together = ("provider", "user_id")
        verbose_name = "OAuth Token"
        verbose_name_plural = "OAuth Tokens"

    def __str__(self) -> str:
        """Return the name of the OAuth token."""
        return f"{self.provider} ({self.name}) @ {self.owner}"

    @property
    def is_expired(self) -> bool:
        """Check if the token has expired."""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

    @property
    def expires_in_humanized(self) -> str:
        """Return the expiration time in humanized format."""
        if not self.expires_at:
            return "Never"
        return naturaltime(self.expires_at)

    @property
    def username(self) -> str:
        """Return the username associated with the OAuth token."""
        return self.profile_json.get("username", "") or self.profile_json.get("login", "") or self.name
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def get_decrypted_access_token(self) -> str:
        """Explicitly get decrypted access token (for debugging/admin)."""
        # This method provides explicit access to decrypted tokens
        # Useful for admin interfaces or debugging
        return self.access_token
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def get_decrypted_refresh_token(self) -> str:
        """Explicitly get decrypted refresh token (for debugging/admin)."""
        return self.refresh_token
```

### Migration for Existing Tokens
```python
# oauth2_capture/migrations/XXXX_encrypt_existing_tokens.py
from django.db import migrations
from django.conf import settings

def encrypt_existing_tokens(apps, schema_editor):
    """Encrypt existing plain text tokens."""
    OAuthToken = apps.get_model('oauth2_capture', 'OAuthToken')
<<<<<<< HEAD
    
    # Only run if encryption is enabled
    if not getattr(settings, 'OAUTH2_ENCRYPT_TOKENS', True):
        return
    
    # Import encryption functions
    from oauth2_capture.encryption import encrypt_token, is_token_encrypted
    
    tokens_updated = 0
    tokens_failed = 0
    
=======

    # Only run if encryption is enabled
    if not getattr(settings, 'OAUTH2_ENCRYPT_TOKENS', True):
        return

    # Import encryption functions
    from oauth2_capture.encryption import encrypt_token, is_token_encrypted

    tokens_updated = 0
    tokens_failed = 0

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    for token in OAuthToken.objects.all():
        try:
            # Encrypt access token if not already encrypted
            if token.access_token and not is_token_encrypted(token.access_token):
                token.access_token = encrypt_token(token.access_token)
<<<<<<< HEAD
            
            # Encrypt refresh token if not already encrypted
            if token.refresh_token and not is_token_encrypted(token.refresh_token):
                token.refresh_token = encrypt_token(token.refresh_token)
            
            token.save()
            tokens_updated += 1
            
        except Exception as e:
            print(f"Failed to encrypt token {token.id}: {str(e)}")
            tokens_failed += 1
    
=======

            # Encrypt refresh token if not already encrypted
            if token.refresh_token and not is_token_encrypted(token.refresh_token):
                token.refresh_token = encrypt_token(token.refresh_token)

            token.save()
            tokens_updated += 1

        except Exception as e:
            print(f"Failed to encrypt token {token.id}: {str(e)}")
            tokens_failed += 1

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    print(f"Token encryption complete: {tokens_updated} updated, {tokens_failed} failed")

def decrypt_existing_tokens(apps, schema_editor):
    """Decrypt tokens back to plain text (reverse migration)."""
    OAuthToken = apps.get_model('oauth2_capture', 'OAuthToken')
<<<<<<< HEAD
    
    from oauth2_capture.encryption import decrypt_token, is_token_encrypted
    
    tokens_updated = 0
    tokens_failed = 0
    
=======

    from oauth2_capture.encryption import decrypt_token, is_token_encrypted

    tokens_updated = 0
    tokens_failed = 0

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    for token in OAuthToken.objects.all():
        try:
            # Decrypt access token if encrypted
            if token.access_token and is_token_encrypted(token.access_token):
                token.access_token = decrypt_token(token.access_token)
<<<<<<< HEAD
            
            # Decrypt refresh token if encrypted
            if token.refresh_token and is_token_encrypted(token.refresh_token):
                token.refresh_token = decrypt_token(token.refresh_token)
            
            token.save()
            tokens_updated += 1
            
        except Exception as e:
            print(f"Failed to decrypt token {token.id}: {str(e)}")
            tokens_failed += 1
    
    print(f"Token decryption complete: {tokens_updated} updated, {tokens_failed} failed")

class Migration(migrations.Migration):
    
    dependencies = [
        ('oauth2_capture', '0002_alter_oauthtoken_access_token'),
    ]
    
=======

            # Decrypt refresh token if encrypted
            if token.refresh_token and is_token_encrypted(token.refresh_token):
                token.refresh_token = decrypt_token(token.refresh_token)

            token.save()
            tokens_updated += 1

        except Exception as e:
            print(f"Failed to decrypt token {token.id}: {str(e)}")
            tokens_failed += 1

    print(f"Token decryption complete: {tokens_updated} updated, {tokens_failed} failed")

class Migration(migrations.Migration):

    dependencies = [
        ('oauth2_capture', '0002_alter_oauthtoken_access_token'),
    ]

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    operations = [
        migrations.RunPython(
            encrypt_existing_tokens,
            decrypt_existing_tokens,
            elidable=True,
        ),
    ]
```

### Management Command for Key Rotation
```python
# oauth2_capture/management/commands/rotate_encryption_keys.py
from django.core.management.base import BaseCommand
from django.db import transaction
from oauth2_capture.models import OAuthToken
from oauth2_capture.encryption import TokenEncryption, decrypt_token
import os

class Command(BaseCommand):
    help = 'Rotate encryption keys for OAuth tokens'
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def add_arguments(self, parser):
        parser.add_argument(
            '--new-key',
            type=str,
            help='New encryption key (base64 encoded)',
            required=True
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes'
        )
<<<<<<< HEAD
    
    def handle(self, *args, **options):
        new_key_b64 = options['new_key']
        dry_run = options['dry_run']
        
=======

    def handle(self, *args, **options):
        new_key_b64 = options['new_key']
        dry_run = options['dry_run']

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        try:
            # Validate new key
            import base64
            new_key = base64.urlsafe_b64decode(new_key_b64.encode())
            new_encryption = TokenEncryption(new_key)
<<<<<<< HEAD
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Invalid new key: {str(e)}"))
            return
        
        # Get current encryption instance
        from oauth2_capture.encryption import get_encryption
        current_encryption = get_encryption()
        
        tokens_to_update = OAuthToken.objects.all()
        total_tokens = tokens_to_update.count()
        
        self.stdout.write(f"Found {total_tokens} tokens to re-encrypt")
        
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - No changes will be made"))
            return
        
        updated_count = 0
        failed_count = 0
        
=======

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Invalid new key: {str(e)}"))
            return

        # Get current encryption instance
        from oauth2_capture.encryption import get_encryption
        current_encryption = get_encryption()

        tokens_to_update = OAuthToken.objects.all()
        total_tokens = tokens_to_update.count()

        self.stdout.write(f"Found {total_tokens} tokens to re-encrypt")

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - No changes will be made"))
            return

        updated_count = 0
        failed_count = 0

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        with transaction.atomic():
            for token in tokens_to_update:
                try:
                    # Decrypt with old key
                    if token.access_token:
                        decrypted_access = current_encryption.decrypt(token.access_token)
                        # Re-encrypt with new key
                        token.access_token = new_encryption.encrypt(decrypted_access)
<<<<<<< HEAD
                    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
                    if token.refresh_token:
                        decrypted_refresh = current_encryption.decrypt(token.refresh_token)
                        # Re-encrypt with new key
                        token.refresh_token = new_encryption.encrypt(decrypted_refresh)
<<<<<<< HEAD
                    
                    token.save()
                    updated_count += 1
                    
                    if updated_count % 100 == 0:
                        self.stdout.write(f"Updated {updated_count}/{total_tokens} tokens...")
                        
=======

                    token.save()
                    updated_count += 1

                    if updated_count % 100 == 0:
                        self.stdout.write(f"Updated {updated_count}/{total_tokens} tokens...")

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Failed to update token {token.id}: {str(e)}")
                    )
                    failed_count += 1
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        self.stdout.write(
            self.style.SUCCESS(
                f"Key rotation complete: {updated_count} updated, {failed_count} failed"
            )
        )
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        if failed_count == 0:
            self.stdout.write(
                self.style.SUCCESS(
                    "All tokens successfully re-encrypted. "
                    "You can now update your OAUTH2_ENCRYPTION_KEY setting."
                )
            )
```

### Configuration Settings
```python
# Settings for token encryption
# Add to your Django settings.py

# Enable/disable token encryption (default: True)
OAUTH2_ENCRYPT_TOKENS = True

# Optional: Use dedicated encryption key instead of deriving from SECRET_KEY
# OAUTH2_ENCRYPTION_KEY = os.environ.get('OAUTH2_ENCRYPTION_KEY')

# Optional: Encryption algorithm settings (advanced)
# OAUTH2_ENCRYPTION_ALGORITHM = 'fernet'  # Currently only supports fernet
```

### Encryption Tests
```python
# oauth2_capture/tests/test_encryption.py
from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from oauth2_capture.models import OAuthToken
from oauth2_capture.encryption import (
    TokenEncryption, encrypt_token, decrypt_token, is_token_encrypted
)
from oauth2_capture.fields import EncryptedTextField, EncryptedCharField
from .fixtures import OAuthTestData

class TokenEncryptionTests(TestCase):
<<<<<<< HEAD
    
    def setUp(self):
        self.encryption = TokenEncryption()
        self.test_token = "test_access_token_12345"
        
=======

    def setUp(self):
        self.encryption = TokenEncryption()
        self.test_token = "test_access_token_12345"

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_encrypt_decrypt_roundtrip(self):
        """Test that encryption and decryption work correctly."""
        encrypted = self.encryption.encrypt(self.test_token)
        decrypted = self.encryption.decrypt(encrypted)
<<<<<<< HEAD
        
        self.assertNotEqual(encrypted, self.test_token)
        self.assertEqual(decrypted, self.test_token)
    
=======

        self.assertNotEqual(encrypted, self.test_token)
        self.assertEqual(decrypted, self.test_token)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_encrypted_token_detection(self):
        """Test detection of encrypted vs plain text tokens."""
        plain_token = "plain_text_token"
        encrypted_token = self.encryption.encrypt(plain_token)
<<<<<<< HEAD
        
        self.assertFalse(is_token_encrypted(plain_token))
        self.assertTrue(is_token_encrypted(encrypted_token))
    
=======

        self.assertFalse(is_token_encrypted(plain_token))
        self.assertTrue(is_token_encrypted(encrypted_token))

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_empty_token_handling(self):
        """Test handling of empty/None tokens."""
        self.assertEqual(encrypt_token(""), "")
        self.assertEqual(encrypt_token(None), None)
        self.assertEqual(decrypt_token(""), "")
        self.assertEqual(decrypt_token(None), None)
<<<<<<< HEAD
    
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_encryption_consistency(self):
        """Test that encryption is consistent but unique."""
        token1 = self.encryption.encrypt(self.test_token)
        token2 = self.encryption.encrypt(self.test_token)
<<<<<<< HEAD
        
        # Different ciphertext (due to random IV)
        self.assertNotEqual(token1, token2)
        
=======

        # Different ciphertext (due to random IV)
        self.assertNotEqual(token1, token2)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # But same plaintext
        self.assertEqual(
            self.encryption.decrypt(token1),
            self.encryption.decrypt(token2)
        )

class EncryptedFieldTests(TestCase):
<<<<<<< HEAD
    
    def setUp(self):
        self.user = OAuthTestData.create_test_user()
    
=======

    def setUp(self):
        self.user = OAuthTestData.create_test_user()

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @override_settings(OAUTH2_ENCRYPT_TOKENS=True)
    def test_encrypted_token_storage(self):
        """Test that tokens are encrypted when stored."""
        token = OAuthToken.objects.create(
            provider='test',
            user_id='123',
            access_token='plain_access_token',
            refresh_token='plain_refresh_token',
            owner=self.user
        )
<<<<<<< HEAD
        
        # Refresh from database to get stored values
        token.refresh_from_db()
        
        # Values should be transparently decrypted
        self.assertEqual(token.access_token, 'plain_access_token')
        self.assertEqual(token.refresh_token, 'plain_refresh_token')
        
=======

        # Refresh from database to get stored values
        token.refresh_from_db()

        # Values should be transparently decrypted
        self.assertEqual(token.access_token, 'plain_access_token')
        self.assertEqual(token.refresh_token, 'plain_refresh_token')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # But stored values in database should be encrypted
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT access_token, refresh_token FROM oauth2_capture_oauthtoken WHERE id = %s",
                [token.id]
            )
            row = cursor.fetchone()
            stored_access, stored_refresh = row
<<<<<<< HEAD
            
            # Stored values should be different from plain text
            self.assertNotEqual(stored_access, 'plain_access_token')
            self.assertNotEqual(stored_refresh, 'plain_refresh_token')
            
            # And should be detectable as encrypted
            self.assertTrue(is_token_encrypted(stored_access))
            self.assertTrue(is_token_encrypted(stored_refresh))
    
=======

            # Stored values should be different from plain text
            self.assertNotEqual(stored_access, 'plain_access_token')
            self.assertNotEqual(stored_refresh, 'plain_refresh_token')

            # And should be detectable as encrypted
            self.assertTrue(is_token_encrypted(stored_access))
            self.assertTrue(is_token_encrypted(stored_refresh))

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    @override_settings(OAUTH2_ENCRYPT_TOKENS=False)
    def test_disabled_encryption(self):
        """Test that encryption can be disabled."""
        token = OAuthToken.objects.create(
            provider='test',
            user_id='123',
            access_token='plain_access_token',
            owner=self.user
        )
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Check database storage directly
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT access_token FROM oauth2_capture_oauthtoken WHERE id = %s",
                [token.id]
            )
            stored_access = cursor.fetchone()[0]
<<<<<<< HEAD
            
            # Should be stored as plain text
            self.assertEqual(stored_access, 'plain_access_token')
    
=======

            # Should be stored as plain text
            self.assertEqual(stored_access, 'plain_access_token')

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_migration_mode_handling(self):
        """Test handling of mixed encrypted/unencrypted tokens during migration."""
        # Create token with migration mode (bypasses encryption)
        from oauth2_capture.fields import EncryptedTextField
<<<<<<< HEAD
        
        field = EncryptedTextField(migration_mode=True)
        
        # Should handle both encrypted and unencrypted values
        encrypted_value = encrypt_token('test_token')
        plain_value = 'plain_token'
        
        # Both should pass through unchanged in migration mode
        self.assertEqual(field.from_db_value(encrypted_value, None, None), encrypted_value)
        self.assertEqual(field.from_db_value(plain_value, None, None), plain_value)
    
=======

        field = EncryptedTextField(migration_mode=True)

        # Should handle both encrypted and unencrypted values
        encrypted_value = encrypt_token('test_token')
        plain_value = 'plain_token'

        # Both should pass through unchanged in migration mode
        self.assertEqual(field.from_db_value(encrypted_value, None, None), encrypted_value)
        self.assertEqual(field.from_db_value(plain_value, None, None), plain_value)

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
    def test_field_length_validation(self):
        """Test that encrypted values fit in field lengths."""
        # Long token that might exceed field length when encrypted
        long_token = 'x' * 400
<<<<<<< HEAD
        
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        try:
            token = OAuthToken.objects.create(
                provider='test',
                user_id='123',
                access_token=long_token,
                refresh_token=long_token,
                owner=self.user
            )
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
            # Should be able to read back correctly
            token.refresh_from_db()
            self.assertEqual(token.access_token, long_token)
            self.assertEqual(token.refresh_token, long_token)
<<<<<<< HEAD
            
=======

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        except ValidationError as e:
            # This might fail if encrypted token exceeds field length
            self.assertIn('encryption', str(e).lower())

class EncryptionPerformanceTests(TestCase):
    """Test performance impact of encryption."""
<<<<<<< HEAD
    
    def test_encryption_performance(self):
        """Test that encryption doesn't significantly impact performance."""
        import time
        
        user = OAuthTestData.create_test_user()
        test_token = 'performance_test_token_' * 10  # ~250 chars
        
=======

    def test_encryption_performance(self):
        """Test that encryption doesn't significantly impact performance."""
        import time

        user = OAuthTestData.create_test_user()
        test_token = 'performance_test_token_' * 10  # ~250 chars

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Test encrypted token creation
        start_time = time.time()
        for i in range(100):
            token = OAuthToken(
                provider=f'test{i}',
                user_id=str(i),
                access_token=test_token,
                refresh_token=test_token,
                owner=user
            )
            token.save()
<<<<<<< HEAD
        
        encrypted_time = time.time() - start_time
        
        # Cleanup
        OAuthToken.objects.filter(provider__startswith='test').delete()
        
=======

        encrypted_time = time.time() - start_time

        # Cleanup
        OAuthToken.objects.filter(provider__startswith='test').delete()

>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
        # Test with encryption disabled
        with override_settings(OAUTH2_ENCRYPT_TOKENS=False):
            start_time = time.time()
            for i in range(100):
                token = OAuthToken(
                    provider=f'plain{i}',
                    user_id=str(i),
                    access_token=test_token,
                    refresh_token=test_token,
                    owner=user
                )
                token.save()
<<<<<<< HEAD
            
            plain_time = time.time() - start_time
        
        # Encryption should not be more than 3x slower
        performance_ratio = encrypted_time / plain_time
        self.assertLess(performance_ratio, 3.0, 
=======

            plain_time = time.time() - start_time

        # Encryption should not be more than 3x slower
        performance_ratio = encrypted_time / plain_time
        self.assertLess(performance_ratio, 3.0,
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
                       f"Encryption too slow: {performance_ratio:.2f}x slower than plain text")
```

## Success Criteria
- [ ] Transparent encryption/decryption of access tokens and refresh tokens
- [ ] Configurable encryption (can be enabled/disabled)
- [ ] Secure key derivation and management
- [ ] Migration support for existing plain text tokens
- [ ] Minimal performance impact (<3x slower than plain text)
- [ ] Backward compatibility with existing code
- [ ] Key rotation functionality for security maintenance
- [ ] Comprehensive test coverage including edge cases
<<<<<<< HEAD
- [ ] Documentation for configuration and deployment
=======
- [ ] Documentation for configuration and deployment
>>>>>>> faace65 (Add comprehensive OAuth security, testing, and coverage infrastructure)
