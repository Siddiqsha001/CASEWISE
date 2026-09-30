-- Debug Client Access Issue
-- Run these queries in Supabase SQL Editor to diagnose the problem

-- 1. Check all profiles (users) in the system
SELECT id, email, role, display_name
FROM profiles
ORDER BY created_at DESC;

-- 2. Check the case and its client email
SELECT
  c.id as case_id,
  c.title,
  cl.id as client_record_id,
  cl.email as client_email,
  cl.portal_user_id,
  cl.name as client_name
FROM cases c
LEFT JOIN clients cl ON cl.id = c.client_id
WHERE c.title LIKE '%TechVision%'
ORDER BY c.created_at DESC
LIMIT 5;

-- 3. Check who has access to the case (case_members table)
SELECT
  cm.case_id,
  c.title,
  cm.user_id,
  p.email as member_email,
  p.role as member_account_role,
  cm.member_role as case_role
FROM case_members cm
JOIN cases c ON c.id = cm.case_id
JOIN profiles p ON p.id = cm.user_id
WHERE c.title LIKE '%TechVision%';

-- 4. Find the mismatch - show client account vs case client email
SELECT
  'Case Client Email' as source,
  cl.email as email,
  cl.portal_user_id,
  c.title as case_title
FROM cases c
JOIN clients cl ON cl.id = c.client_id
WHERE c.title LIKE '%TechVision%'
UNION ALL
SELECT
  'Client Profile' as source,
  p.email,
  p.id as profile_id,
  'N/A' as case_title
FROM profiles p
WHERE p.role = 'CLIENT'
ORDER BY source;
