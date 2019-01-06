CREATE TABLE input_cube_edge
(
    ColorCode varchar(2) NOT NULL PRIMARY KEY,
    ColorIndex_x1 int(1) NOT NULL,
    ColorIndex_y1 int(1) NOT NULL,
    ColorIndex_x2 int(1) NOT NULL,
    ColorIndex_y2 int(1) NOT NULL,
    ColorPresent_1 varchar(1) NOT NULL,
    ColorPresent_2 varchar(1) NOT NULL
);

CREATE TABLE input_cube_corner
(
    ColorCode varchar(3) NOT NULL PRIMARY KEY,
    ColorIndex_x1 int(1) NOT NULL,
    ColorIndex_y1 int(1) NOT NULL,
    ColorIndex_x2 int(1) NOT NULL,
    ColorIndex_y2 int(1) NOT NULL,
    ColorIndex_x3 int(1) NOT NULL,
    ColorIndex_y3 int(1) NOT NULL,
    ColorPresent_1 varchar(1) NOT NULL,
    ColorPresent_2 varchar(1) NOT NULL,
    ColorPresent_3 varchar(1) NOT NULL
);

CREATE TABLE solved_cube_edge
(
    ColorCode varchar(2) NOT NULL PRIMARY KEY,
    ColorIndex_x1 int(1) NOT NULL,
    ColorIndex_y1 int(1) NOT NULL,
    ColorIndex_x2 int(1) NOT NULL,
    ColorIndex_y2 int(1) NOT NULL,
    ColorPresent_1 varchar(1) NOT NULL,
    ColorPresent_2 varchar(1) NOT NULL
);

CREATE TABLE solved_cube_corner
(
    ColorCode varchar(3) NOT NULL PRIMARY KEY,
    ColorIndex_x1 int(1) NOT NULL,
    ColorIndex_y1 int(1) NOT NULL,
    ColorIndex_x2 int(1) NOT NULL,
    ColorIndex_y2 int(1) NOT NULL,
    ColorIndex_x3 int(1) NOT NULL,
    ColorIndex_y3 int(1) NOT NULL,
    ColorPresent_1 varchar(1) NOT NULL,
    ColorPresent_2 varchar(1) NOT NULL,
    ColorPresent_3 varchar(1) NOT NULL
);
