import { createClient } from "@supabase/supabase-js";
export const supabase = createClient(import.meta?.env?.SUPABASE_URL || "YOUR_URL",
                                     "YOUR_ANON_KEY");
export async function login(email, password) {
  const { data, error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) throw error; return data;
}
export async function getToken() {
  const { data } = await supabase.auth.getSession();
  return data?.session?.access_token || null;
}
