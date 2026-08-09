CREATE OR REPLACE FUNCTION find_common_availability(
    p_group_id INTEGER,
    p_min_minutes INTEGER DEFAULT 30
)
RETURNS TABLE (
    day_of_week INTEGER,
    day_name TEXT,
    common_start_time TIME,
    common_end_time TIME,
    duration_minutes INTEGER
)
LANGUAGE SQL
AS $$
WITH
-- Gather every availability slot for members of the selected group.
member_slots AS (
    SELECT gm.user_id, a.day_of_week, a.start_time, a.end_time
    FROM group_members gm
    JOIN availability a ON a.user_id = gm.user_id
    WHERE gm.group_id = p_group_id
),
-- Count how many members must be available for a valid overlap.
member_count AS (
    SELECT COUNT(DISTINCT user_id)::INTEGER AS total_members
    FROM member_slots
),
-- Build all possible boundary points for each day.
boundary_points AS (
    SELECT day_of_week, start_time AS time_value FROM member_slots
    UNION
    SELECT day_of_week, end_time AS time_value FROM member_slots
),
-- Create candidate intervals from each pair of boundary points.
candidate_periods AS (
    SELECT
        bp1.day_of_week,
        bp1.time_value AS common_start_time,
        bp2.time_value AS common_end_time
    FROM boundary_points bp1
    JOIN boundary_points bp2
      ON bp2.day_of_week = bp1.day_of_week
     AND bp2.time_value > bp1.time_value
),
-- Keep only intervals covered by at least one slot for every member.
valid_periods AS (
    SELECT
        cp.day_of_week,
        cp.common_start_time,
        cp.common_end_time
    FROM candidate_periods cp
    CROSS JOIN member_count mc
    WHERE (
        SELECT COUNT(DISTINCT ms.user_id)
        FROM member_slots ms
        WHERE ms.day_of_week = cp.day_of_week
          AND ms.start_time <= cp.common_start_time
          AND ms.end_time >= cp.common_end_time
    ) = mc.total_members
)
SELECT
    vp.day_of_week,
    CASE vp.day_of_week
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
        WHEN 7 THEN 'Sunday'
    END AS day_name,
    vp.common_start_time,
    vp.common_end_time,
    CAST(EXTRACT(EPOCH FROM (vp.common_end_time - vp.common_start_time)) / 60 AS INTEGER) AS duration_minutes
FROM valid_periods vp
WHERE CAST(EXTRACT(EPOCH FROM (vp.common_end_time - vp.common_start_time)) / 60 AS INTEGER) >= p_min_minutes
ORDER BY vp.day_of_week, vp.common_start_time;
$$;
