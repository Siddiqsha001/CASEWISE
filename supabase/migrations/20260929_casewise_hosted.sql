-- Hosted Supabase schema. Apply only to a new/empty CaseWise project.
-- Uses Supabase auth.uid() and authenticated role.
CREATE TABLE profiles (
  id uuid PRIMARY KEY,
  email text NOT NULL,
  display_name text NOT NULL DEFAULT '',
  role text NOT NULL CHECK (role IN ('LAWYER', 'CLIENT')),
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE clients (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  kind text NOT NULL DEFAULT 'INDIVIDUAL' CHECK (kind IN ('INDIVIDUAL','ORGANIZATION')),
  name text NOT NULL,
  phone text,
  email text,
  address text,
  portal_user_id uuid REFERENCES profiles(id),
  created_by uuid NOT NULL REFERENCES profiles(id),
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE cases (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  title text NOT NULL,
  case_number text,
  case_type text,
  court text,
  status text NOT NULL DEFAULT 'DRAFT' CHECK (status IN ('DRAFT','ACTIVE','CLOSED')),
  priority text NOT NULL DEFAULT 'NORMAL' CHECK (priority IN ('LOW','NORMAL','HIGH')),
  filing_date date,
  client_id uuid REFERENCES clients(id),
  main_issue text,
  description text,
  created_by uuid NOT NULL REFERENCES profiles(id),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE case_members (
  case_id uuid NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  user_id uuid NOT NULL REFERENCES profiles(id),
  member_role text NOT NULL CHECK (member_role IN ('LAWYER','CLIENT')),
  created_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY(case_id,user_id)
);
CREATE TABLE opposing_parties (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), case_id uuid NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  kind text NOT NULL DEFAULT 'ORGANIZATION', name text NOT NULL, contact text, address text, counsel text
);
CREATE TABLE documents (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), case_id uuid NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  file_name text NOT NULL, mime_type text NOT NULL, byte_size bigint NOT NULL,
  storage_path text NOT NULL, processing_status text NOT NULL DEFAULT 'UPLOADED',
  error_message text, visibility text NOT NULL DEFAULT 'LAWYER_ONLY' CHECK (visibility IN ('LAWYER_ONLY','CLIENT_SHARED')),
  uploaded_by uuid NOT NULL REFERENCES profiles(id), created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE document_chunks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), case_id uuid NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  document_id uuid NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  page_number integer, section text, content text NOT NULL, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE claims (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), case_id uuid NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  statement text NOT NULL, source_chunk_id uuid REFERENCES document_chunks(id), status text NOT NULL DEFAULT 'SUGGESTED',
  visibility text NOT NULL DEFAULT 'LAWYER_ONLY', created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE evidence (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), case_id uuid NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  name text NOT NULL, type text, description text, source_document_id uuid REFERENCES documents(id), source_page integer,
  status text NOT NULL DEFAULT 'SUGGESTED', visibility text NOT NULL DEFAULT 'LAWYER_ONLY', notes text,
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE claim_evidence (
  claim_id uuid NOT NULL REFERENCES claims(id) ON DELETE CASCADE,
  evidence_id uuid NOT NULL REFERENCES evidence(id) ON DELETE CASCADE,
  relationship text NOT NULL DEFAULT 'SUPPORTS', PRIMARY KEY(claim_id,evidence_id)
);
CREATE TABLE timeline_events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), case_id uuid NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  event_date date, description text NOT NULL, source_chunk_id uuid REFERENCES document_chunks(id),
  status text NOT NULL DEFAULT 'SUGGESTED', visibility text NOT NULL DEFAULT 'LAWYER_ONLY', created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE contradictions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), case_id uuid NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  source_a_chunk_id uuid REFERENCES document_chunks(id), source_b_chunk_id uuid REFERENCES document_chunks(id),
  description text NOT NULL, review_status text NOT NULL DEFAULT 'SUGGESTED', visibility text NOT NULL DEFAULT 'LAWYER_ONLY',
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE hearings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), case_id uuid NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  starts_at timestamptz NOT NULL, court text, purpose text, notes text, status text NOT NULL DEFAULT 'SCHEDULED',
  visibility text NOT NULL DEFAULT 'CLIENT_SHARED', created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE tasks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), case_id uuid NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  title text NOT NULL, assignee_id uuid REFERENCES profiles(id), due_at timestamptz,
  status text NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING','IN_PROGRESS','COMPLETED')),
  visibility text NOT NULL DEFAULT 'LAWYER_ONLY', created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE payments (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), case_id uuid NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  total_fee numeric(12,2) NOT NULL DEFAULT 0, amount_paid numeric(12,2) NOT NULL DEFAULT 0,
  currency text NOT NULL DEFAULT 'INR', due_date date, status text NOT NULL DEFAULT 'PENDING',
  visibility text NOT NULL DEFAULT 'LAWYER_ONLY', created_at timestamptz NOT NULL DEFAULT now(),
  CHECK (total_fee >= 0 AND amount_paid >= 0)
);
CREATE TABLE notifications (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), recipient_id uuid NOT NULL REFERENCES profiles(id),
  case_id uuid REFERENCES cases(id) ON DELETE CASCADE, kind text NOT NULL, message text NOT NULL,
  read_at timestamptz, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE ai_analyses (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), case_id uuid NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  kind text NOT NULL, result jsonb NOT NULL DEFAULT '{}'::jsonb, status text NOT NULL DEFAULT 'SUGGESTED',
  visibility text NOT NULL DEFAULT 'LAWYER_ONLY', model text, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE case_notes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), case_id uuid NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  author_id uuid NOT NULL REFERENCES profiles(id), body text NOT NULL, visibility text NOT NULL DEFAULT 'LAWYER_ONLY',
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE activity_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(), case_id uuid NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
  actor_id uuid NOT NULL REFERENCES profiles(id), action text NOT NULL, entity_type text NOT NULL,
  entity_id uuid, created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX ON case_members(user_id,case_id);
CREATE INDEX ON documents(case_id,processing_status);
CREATE INDEX ON document_chunks(case_id,document_id);
CREATE INDEX ON hearings(case_id,starts_at);
CREATE INDEX ON tasks(case_id,due_at);

CREATE FUNCTION is_case_lawyer(p_case uuid) RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path=public AS $$
  SELECT EXISTS (SELECT 1 FROM case_members WHERE case_id=p_case AND user_id=auth.uid() AND member_role='LAWYER')
$$;
CREATE FUNCTION is_case_member(p_case uuid) RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path=public AS $$
  SELECT EXISTS (SELECT 1 FROM case_members WHERE case_id=p_case AND user_id=auth.uid())
$$;

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
CREATE POLICY profiles_read ON profiles FOR SELECT TO authenticated USING (id=auth.uid());
CREATE POLICY profiles_case_client_lookup ON profiles FOR SELECT TO authenticated USING (
  role='CLIENT' AND EXISTS (
    SELECT 1 FROM cases c JOIN clients cl ON cl.id=c.client_id
    WHERE is_case_lawyer(c.id) AND lower(cl.email)=lower(profiles.email)
  )
);
CREATE POLICY profiles_insert ON profiles FOR INSERT TO authenticated WITH CHECK (id=auth.uid());
ALTER TABLE clients ENABLE ROW LEVEL SECURITY;
CREATE POLICY clients_read ON clients FOR SELECT TO authenticated USING (created_by=auth.uid() OR portal_user_id=auth.uid());
CREATE POLICY clients_insert ON clients FOR INSERT TO authenticated WITH CHECK (created_by=auth.uid());
CREATE POLICY clients_update ON clients FOR UPDATE TO authenticated USING (created_by=auth.uid()) WITH CHECK (created_by=auth.uid());
ALTER TABLE cases ENABLE ROW LEVEL SECURITY;
CREATE POLICY cases_select ON cases FOR SELECT TO authenticated USING (is_case_member(id) OR created_by=auth.uid());
CREATE POLICY cases_insert ON cases FOR INSERT TO authenticated WITH CHECK (created_by=auth.uid() AND EXISTS (SELECT 1 FROM profiles WHERE id=auth.uid() AND role='LAWYER'));
CREATE POLICY cases_update ON cases FOR UPDATE TO authenticated USING (is_case_lawyer(id)) WITH CHECK (is_case_lawyer(id));
ALTER TABLE case_members ENABLE ROW LEVEL SECURITY;
CREATE POLICY members_select ON case_members FOR SELECT TO authenticated USING (is_case_member(case_id));
CREATE POLICY members_insert ON case_members FOR INSERT TO authenticated WITH CHECK (user_id=auth.uid() AND member_role='LAWYER' AND EXISTS (SELECT 1 FROM cases WHERE id=case_id AND created_by=auth.uid()));
CREATE POLICY members_client_invite ON case_members FOR INSERT TO authenticated WITH CHECK (
  member_role='CLIENT' AND is_case_lawyer(case_id) AND EXISTS (
    SELECT 1 FROM cases c JOIN clients cl ON cl.id=c.client_id JOIN profiles p ON p.id=user_id
    WHERE c.id=case_id AND p.role='CLIENT' AND lower(p.email)=lower(cl.email)
  )
);

DO $$ DECLARE t text; BEGIN
  FOREACH t IN ARRAY ARRAY['opposing_parties','documents','document_chunks','claims','evidence','timeline_events','contradictions','hearings','tasks','payments','ai_analyses','case_notes','activity_logs'] LOOP
    EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY',t);
    EXECUTE format('CREATE POLICY %I_read ON %I FOR SELECT TO authenticated USING (is_case_lawyer(case_id) OR (is_case_member(case_id) AND %s))',t,t,
      CASE WHEN t IN ('opposing_parties','document_chunks','activity_logs') THEN 'false'
           WHEN t='tasks' THEN '(visibility=''CLIENT_SHARED'' OR assignee_id=auth.uid())'
           ELSE 'visibility=''CLIENT_SHARED''' END);
    IF t NOT IN ('document_chunks','activity_logs') THEN
      EXECUTE format('CREATE POLICY %I_write ON %I FOR ALL TO authenticated USING (is_case_lawyer(case_id)) WITH CHECK (is_case_lawyer(case_id))',t,t);
    END IF;
  END LOOP;
END $$;
CREATE POLICY chunks_write ON document_chunks FOR ALL TO authenticated USING (is_case_lawyer(case_id)) WITH CHECK (is_case_lawyer(case_id));
CREATE POLICY logs_write ON activity_logs FOR INSERT TO authenticated WITH CHECK (is_case_lawyer(case_id) AND actor_id=auth.uid());
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
CREATE POLICY notifications_own ON notifications FOR ALL TO authenticated USING (recipient_id=auth.uid()) WITH CHECK (recipient_id=auth.uid());
ALTER TABLE claim_evidence ENABLE ROW LEVEL SECURITY;
CREATE POLICY claim_evidence_lawyer ON claim_evidence FOR ALL TO authenticated USING (EXISTS (SELECT 1 FROM claims c WHERE c.id=claim_id AND is_case_lawyer(c.case_id))) WITH CHECK (EXISTS (SELECT 1 FROM claims c JOIN evidence e ON e.id=evidence_id AND e.case_id=c.case_id WHERE c.id=claim_id AND is_case_lawyer(c.case_id)));

GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO authenticated;

ALTER TABLE profiles ADD CONSTRAINT profiles_auth_user_fk FOREIGN KEY (id) REFERENCES auth.users(id) ON DELETE CASCADE;
CREATE TABLE casewise_schema_migrations (
  version text PRIMARY KEY,
  applied_at timestamptz NOT NULL DEFAULT now()
);
INSERT INTO casewise_schema_migrations(version) VALUES ('20260929_casewise_hosted');
