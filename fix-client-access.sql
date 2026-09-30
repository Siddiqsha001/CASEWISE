-- FIX CLIENT ACCESS FOR TECHVISION CASE
-- Run these queries one by one in Supabase SQL Editor

-- STEP 1: Verify the client profile exists
SELECT id, email, role, display_name, created_at
FROM profiles
WHERE email = 'siddiqsha.a2023aiml@sece.ac.in';
-- ⚠️ If this returns NO ROWS, the client account doesn't exist!
-- You need to sign up with that email first.

-- STEP 2: Check the case and client details
SELECT
  c.id as case_id,
  c.title,
  cl.id as client_id,
  cl.email as client_email,
  cl.portal_user_id
FROM cases c
LEFT JOIN clients cl ON cl.id = c.client_id
WHERE c.title LIKE '%TechVision%'
ORDER BY c.created_at DESC
LIMIT 1;

-- STEP 3: Check current case_members (who already has access)
SELECT
  cm.case_id,
  cm.user_id,
  p.email,
  cm.member_role
FROM case_members cm
JOIN profiles p ON p.id = cm.user_id
WHERE cm.case_id IN (
  SELECT id FROM cases WHERE title LIKE '%TechVision%'
);

-- STEP 4: MANUALLY GRANT ACCESS
-- This will insert the client into case_members
INSERT INTO case_members (case_id, user_id, member_role)
SELECT
  c.id as case_id,
  p.id as user_id,
  'CLIENT' as member_role
FROM cases c
CROSS JOIN profiles p
WHERE c.title LIKE '%TechVision%'
  AND p.email = 'siddiqsha.a2023aiml@sece.ac.in'
  AND p.role = 'CLIENT'
  AND NOT EXISTS (
    SELECT 1 FROM case_members cm
    WHERE cm.case_id = c.id AND cm.user_id = p.id
  )
ORDER BY c.created_at DESC
LIMIT 1;

-- STEP 5: Update client's portal_user_id (links client record to profile)
UPDATE clients
SET portal_user_id = (
  SELECT id FROM profiles WHERE email = 'siddiqsha.a2023aiml@sece.ac.in' AND role = 'CLIENT'
)
WHERE id IN (
  SELECT client_id FROM cases WHERE title LIKE '%TechVision%'
)
AND portal_user_id IS NULL;

-- STEP 6: VERIFY THE FIX - Check case_members again
SELECT
  c.title,
  p.email,
  p.role,
  cm.member_role
FROM case_members cm
JOIN cases c ON c.id = cm.case_id
JOIN profiles p ON p.id = cm.user_id
WHERE c.title LIKE '%TechVision%';
-- ✅ You should now see TWO rows:
--    1. siddianand2005@gmail.com - LAWYER
--    2. siddiqsha.a2023aiml@sece.ac.in - CLIENT
