-- Create test user for Smart AI
-- Password: TestPass123! (hashed with bcrypt)

-- Insert test user
INSERT INTO users (id, email, full_name, password_hash, role, is_active, is_verified, created_at, updated_at)
VALUES (
    gen_random_uuid(),
    'test@smartai.com',
    'Test User',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIWXQXqJUe',  -- TestPass123!
    'user',
    true,
    true,
    NOW(),
    NOW()
)
ON CONFLICT (email) DO NOTHING
RETURNING id, email, full_name, role, is_active, is_verified, created_at;

-- Get the user ID for profile creation
DO $$
DECLARE
    user_uuid UUID;
BEGIN
    -- Get the user ID
    SELECT id INTO user_uuid FROM users WHERE email = 'test@smartai.com';

    -- Insert user profile
    INSERT INTO user_profiles (
        user_id,
        date_of_birth,
        gender,
        emergency_contact_name,
        emergency_contact_phone,
        timezone,
        language_preference,
        created_at,
        updated_at
    )
    VALUES (
        user_uuid,
        '1950-01-01',
        'other',
        'Emergency Contact',
        '+1234567890',
        'America/New_York',
        'en',
        NOW(),
        NOW()
    )
    ON CONFLICT (user_id) DO NOTHING;
END $$;

-- Verify test user was created
SELECT
    u.id,
    u.email,
    u.full_name,
    u.role,
    u.is_active,
    u.is_verified,
    u.created_at,
    up.timezone,
    up.language_preference
FROM users u
LEFT JOIN user_profiles up ON u.id = up.user_id
WHERE u.email = 'test@smartai.com';
