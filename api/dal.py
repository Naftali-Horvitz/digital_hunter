from connection import get_conn

conn = get_conn()

quality_goal_shift_alert = """
    SELECT entity_id, target_name, priority_level, movement_distance_km
    FROM targets 
    WHERE (priority_level = 1 or priority_level = 2) and movement_distance_km > 5
    """

analysis_collection_sources = """
    SELECT signal_type , COUNT(signal_type) AS count_signals
    FROM intel_signals
    group by signal_type 
    ORDER BY count_signals DESC
    """

finding_new_targets = """
    SELECT entity_id , COUNT(entity_id) AS count_new_goals
    FROM intel_signals
    WHERE priority_level = 99 or entity_id LIKE 'UNKNOWN'
    group by entity_id 
    ORDER BY count_new_goals DESC
    LIMIT 3
    """

extreme_behavioral_pattern = """
    SELECT * FROM (SELECT i1.entity_id,
    SUM(111.111 *
    DEGREES(ACOS(LEAST(1.0, COS(RADIANS(i1.reported_lat))
    * COS(RADIANS(i2.reported_lat))
    * COS(RADIANS(i1.reported_lon - i2.reported_lon))
    + SIN(RADIANS(i1.reported_lat))
    * SIN(RADIANS(i2.reported_lat)))))) AS distance_in_km
    FROM intel_signals as i1
    INNER JOIN intel_signals as i2
    on i1.entity_id =  i2.entity_id
    WHERE HOUR(i1.timestamp) BETWEEN 8 AND 19
    GROUP BY i1.entity_id
    HAVING distance_in_km <= 0
    ) AS day
    
    INNER JOIN
    (SELECT i1.entity_id,
    SUM(111.111 *
    DEGREES(ACOS(LEAST(1.0, COS(RADIANS(i1.reported_lat))
    * COS(RADIANS(i2.reported_lat))
    * COS(RADIANS(i1.reported_lon - i2.reported_lon))
    + SIN(RADIANS(i1.reported_lat))
    * SIN(RADIANS(i2.reported_lat)))))) AS distance_in_km
    FROM intel_signals as i1
    INNER JOIN intel_signals as i2
    on i1.entity_id =  i2.entity_id
    WHERE HOUR(i1.timestamp) BETWEEN 0 AND 7 or HOUR(i1.timestamp) BETWEEN 20 AND 23
    GROUP BY i1.entity_id
    HAVING distance_in_km <= 0
    ) AS night
    ON day.entity_id = night.entity_id
    """
    
all_entities = """
SELECT max(entity_id) as entities
FROM intel_signals
GROUP BY entity_id
"""


def run_query(query: str):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def load_target_path(entity_id: str):
    query = f"""
        SELECT reported_lon, reported_lat
        FROM intel_signals
        WHERE entity_id = '{entity_id}'
        """
    return run_query(query)
