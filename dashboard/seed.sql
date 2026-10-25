-- Synthetic usage traffic for LOCAL development only. Never run against production.
--   cd dashboard && bun run seed
-- Re-running replaces all usage_events.
CREATE TABLE IF NOT EXISTS usage_events (
  id serial PRIMARY KEY,
  timestamp timestamptz NOT NULL DEFAULT now(),
  event_type varchar NOT NULL,
  name varchar NOT NULL,
  theme varchar,
  client varchar,
  latency_ms integer,
  response_chars integer,
  error varchar
);
CREATE INDEX IF NOT EXISTS ix_usage_events_timestamp ON usage_events (timestamp);
TRUNCATE usage_events RESTART IDENTITY;

INSERT INTO usage_events (timestamp, event_type, name, theme, client, latency_ms, response_chars, error)
SELECT
  ts,
  CASE WHEN r_type < 0.30 THEN 'resource_read' ELSE 'tool_call' END,
  CASE
    WHEN r_type < 0.30 THEN (ARRAY['slidev://guide/syntax','slidev://themes/guide','slidev://themes/installed','slidev://builtin/layouts','slidev://examples/minimal','slides://session/{uuid}','slidev://themes/seriph','slidev://themes/dracula'])[1 + floor(random()*8)::int]
    WHEN r_tool < 0.38 THEN 'render_slides'
    WHEN r_tool < 0.52 THEN 'get_theme'
    WHEN r_tool < 0.64 THEN 'list_themes'
    WHEN r_tool < 0.74 THEN 'get_slidev_guide'
    WHEN r_tool < 0.82 THEN 'screenshot_slides'
    WHEN r_tool < 0.89 THEN 'export_slides'
    WHEN r_tool < 0.95 THEN 'browse_themes'
    ELSE 'list_session_slides'
  END AS name,
  CASE WHEN r_type >= 0.30 AND r_tool < 0.52 THEN theme END,
  client,
  (60 + (-ln(1 - random()) * CASE WHEN r_tool < 0.38 THEN 6000 ELSE 300 END))::int,
  (800 + floor(random() * 9000))::int,
  CASE WHEN r_type >= 0.30 AND r_tool < 0.38 AND random() < 0.05
       THEN (ARRAY['build_timeout','build_failed','concurrent_limit','theme_not_allowed'])[1 + floor(random()*4)::int]
       WHEN random() < 0.004 THEN 'not_found' END
FROM (
  SELECT
    ts,
    random() AS r_type,
    random() AS r_tool,
    (ARRAY['neocarbon','neocarbon','default','default','dracula','seriph','apple-basic','frankfurt','academic','nord','geist','penguin'])[1 + floor(random()*12)::int] AS theme,
    (ARRAY['claude-ai','claude-ai','claude-ai','claude-code','claude-code','cursor','cursor','visual-studio-code','chatgpt','mcp-remote','zed'])[1 + floor(random()*11)::int] AS client
  FROM (
    SELECT now() - make_interval(secs => random() * 30 * 86400) AS ts
    FROM generate_series(1, 9000)
  ) raw
  WHERE random() < (0.35 + 0.65 * (1 - extract(epoch FROM (now() - ts)) / (30 * 86400)))
    AND (extract(isodow FROM ts) < 6 OR random() < 0.5)
) t;

SELECT count(*) AS seeded_events, min(timestamp)::date AS first_day, max(timestamp)::date AS last_day FROM usage_events;
