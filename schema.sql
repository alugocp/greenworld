
-- The plants that are focused on in this project
CREATE TABLE plants(
  id INT, -- primary key
  species TEXT, -- scientific name
  common TEXT -- common name
);

-- The developmental stages of a plant
CREATE TABLE stages(
  plant INT, -- foreign key, primary key
  order INT, -- order within the plant's developmental stages
  common TEXT, -- common name
  duration INT, -- average duration in days (or some other unit)
  needs JSON, -- map of the plant's nutritional needs at this stage
  gives JSON -- map of the plant's nutritional content at this stage
  -- List of diseases this plant is susceptible to at this stage
);

-- The auxiliary species involved in companionship systems
CREATE TABLE auxiliaries(
  id INT, -- primary key
  species TEXT, -- scientific name
  common TEXT, -- common name
  needs JSON, -- map of the species's nutritional needs
  gives JSON -- map of the species's nutritional content
  -- List of diseases this species can cause
);

-- Super specific species identifier for hierarchy-based searches
CREATE TABLE taxonomies(
  kingdom TEXT;
  phylum TEXT;
  class TEXT;
  order TEXT;
  family TEXT;
  genus TEXT;
  species TEXT;
);