CREATE TABLE biodiversity (
    id INT NOT NULL AUTO_INCREMENT,
    county VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    taxonomic_group VARCHAR(255) NOT NULL,
    taxonomic_subgroup VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255) NOT NULL,
    common_name VARCHAR(255) NOT NULL,
    year_last_documented VARCHAR(255) NOT NULL,
    ny_listing_status VARCHAR(255) NOT NULL,
    federal_listing_status VARCHAR(255) NOT NULL,
    state_conservation_rank VARCHAR(255) NOT NULL,
    global_conservation_rank VARCHAR(255) NOT NULL,
    distribution_status VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

LOAD DATA LOCAL INFILE '/vagrant/biodiversity.csv' INTO TABLE biodiversity FIELDS TERMINATED BY ',' ENCLOSED BY '"' (county,category,taxonomic_group,taxonomic_subgroup,scientific_name,common_name,year_last_documented,ny_listing_status,federal_listing_status,state_conservation_rank,global_conservation_rank,distribution_status);
