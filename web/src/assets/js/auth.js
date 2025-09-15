import { createClient } from "@supabase/supabase-js";

const { SUPABASE_URL, SUPABASE_ANON_KEY } = window.ENV || {};
export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
