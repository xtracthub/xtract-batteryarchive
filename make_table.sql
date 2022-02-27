
CREATE TABLE battery_data (
    id INT PRIMARY KEY NOT NULL,
    filename VARCHAR(250) NOT NULL,
    filesize INT,
    cathode VARCHAR(20),
    anode VARCHAR(20),
    num_cycles INT,
    earliest_dt TIMESTAMP WITHOUT TIME ZONE,
    latest_dt TIMESTAMP WITHOUT TIME ZONE,
    elapsed_s INT,
    group_code VARCHAR(20),
    group_name VARCHAR(100),
    min_temp_c numeric,
    max_temp_c numeric,
    temp_set_c numeric,
    has_nans boolean,
    is_error boolean,
    dvodt_start numeric,
    dvodt_end numeric
)