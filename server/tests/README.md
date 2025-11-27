## Integration Tests 

#### API Level
11/27/2025:
The following tests were added:
1. `test_create_user`
2. `test_duplicate_emails_signup`
With these tests passing, user creation API endpoint correctly works and correctly does not allow signup for an already existing email.

#### DB Level
11/27/2025:
The following tests were added:
1. `test_duplicate_email_is_atomic`
