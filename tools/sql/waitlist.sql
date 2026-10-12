-- Aviso de lançamento do site comandoo.online (projeto Supabase "controley", sa-east-1).
-- O site só chama a função; a tabela não tem política de leitura/escrita para a chave pública.
create table if not exists public.comandoo_waitlist (
  id bigint generated always as identity primary key,
  email text not null,
  lang text not null default 'pt' check (lang in ('pt','en','es')),
  source text,
  created_at timestamptz not null default now(),
  notified_at timestamptz,
  constraint comandoo_waitlist_email_key unique (email)
);
alter table public.comandoo_waitlist enable row level security;

create or replace function public.comandoo_waitlist_join(p_email text, p_lang text default 'pt', p_source text default null)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
declare e text := lower(trim(p_email));
begin
  if e is null or length(e) > 254 or e !~ '^[^@[:space:]]+@[^@[:space:]]+\.[^@[:space:]]+$' then
    raise exception 'invalid_email' using errcode = '22023';
  end if;
  insert into public.comandoo_waitlist (email, lang, source)
  values (e, case when p_lang in ('pt','en','es') then p_lang else 'pt' end, left(p_source, 120))
  on conflict (email) do nothing;
  return true;
end
$$;

revoke all on function public.comandoo_waitlist_join(text, text, text) from public;
grant execute on function public.comandoo_waitlist_join(text, text, text) to anon, authenticated;

-- Política: apagar 30 dias depois do aviso de lançamento.
-- delete from public.comandoo_waitlist where notified_at < now() - interval '30 days';
