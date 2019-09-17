CREATE TABLE listing(
  id INT NOT NULL,
  url VARCHAR NULL,
  name VARCHAR NULL,
  summary VARCHAR NULL,
  space VARCHAR NULL,
  description VARCHAR NULL,
  experiences_offered VARCHAR NULL,
  neighborhood_overview VARCHAR NULL,
  neighbourhood VARCHAR NULL,
  neighbourhood_cleansed SMALLINT NULL,
  neighbourhood_group_cleansed VARCHAR NULL,
  notes VARCHAR NULL,
  transit VARCHAR NULL,
  access VARCHAR NULL,
  interaction VARCHAR NULL,
  house_rules VARCHAR NULL,
  thumbnail_url VARCHAR NULL,
  medium_url VARCHAR NULL,
  picture_url VARCHAR NULL,
  xl_picture_url VARCHAR NULL,
  street VARCHAR NULL,
  city VARCHAR NULL,
  state VARCHAR NULL,
  zipcode SMALLINT NULL,
  market VARCHAR NULL,
  country_code VARCHAR NULL,
  country VARCHAR NULL,
  latitude INT NULL,
  longitude INT NULL,
  is_location_exact BOOLEAN NULL,
  property_type VARCHAR NULL,
  room_type VARCHAR NULL,
  accommodates SMALLINT NULL,
  bathrooms SMALLINT NULL,
  bedrooms SMALLINT NULL,
  beds SMALLINT NULL,
  bed_type VARCHAR NULL,
  amenities JSONB NULL,
  square_feet SMALLINT NULL,
  price SMALLINT NULL,
  weekly_price SMALLINT NULL,
  monthly_price SMALLINT NULL,
  security_deposit SMALLINT NULL,
  cleaning_fee SMALLINT NULL,
  guests_included SMALLINT NULL,
  extra_people SMALLINT NULL,
  minimum_nights SMALLINT NULL,
  maximum_nights SMALLINT NULL,
  minimum_minimum_nights SMALLINT NULL,
  maximum_minimum_nights SMALLINT NULL,
  minimum_maximum_nights SMALLINT NULL,
  maximum_maximum_nights SMALLINT NULL,
  minimum_nights_avg_ntm SMALLINT NULL,
  maximum_nights_avg_ntm SMALLINT NULL,
  calendar_updated VARCHAR NULL,
  has_availability BOOLEAN NULL,
  availability_30 SMALLINT NULL, 
  availability_60 SMALLINT NULL,
  availability_90 SMALLINT NULL,
  availability_365 SMALLINT NULL,
  number_of_reviews SMALLINT NULL,
  number_of_reviews_ltm SMALLINT NULL,
  first_review DATE NULL,
  last_review DATE NULL,
  review_scores_rating SMALLINT NULL,
  review_scores_accuracy SMALLINT NULL,
  review_scores_cleanliness SMALLINT NULL,
  review_scores_checkin SMALLINT NULL,
  review_scores_communication SMALLINT NULL,
  review_scores_location SMALLINT NULL,
  review_scores_value SMALLINT NULL,
  requires_license BOOLEAN NULL,
  instant_bookable BOOLEAN NULL,
  is_business_travel_ready BOOLEAN NULL,
  cancellation_policy VARCHAR NULL,
  require_guest_profile_picture BOOLEAN NULL,
  require_guest_phone_verification BOOLEAN NULL,
  calculated_host_listings_count SMALLINT NULL,
  calculated_host_listings_count_entire_homes SMALLINT NULL,
  calculated_host_listings_count_private_rooms SMALLINT NULL,
  calculated_host_listings_count_shared_rooms SMALLINT NULL,
  reviews_per_month SMALLINT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE host(
  id SMALLINT NOT NULL,
  listing_id SMALLINT NOT NULL,
  url VARCHAR NULL,
  name VARCHAR NOT NULL,
  since DATE NOT NULL,
  city VARCHAR NULL,
  neighborhood VARCHAR NULL,
  country VARCHAR NULL,
  about VARCHAR NULL,
  response_time VARCHAR NULL,
  response_rate SMALLINT NULL,
  acceptance_rate SMALLINT NULL,
  is_superhost BOOLEAN NULL,
  thumbnail_url VARCHAR NULL,
  picture_url VARCHAR NULL,
  neighbourhood VARCHAR NULL,
  listings_count SMALLINT NULL,
  total_listings_count SMALLINT NULL,
  verifications JSONB NULL,
  has_profile_pic BOOLEAN NULL,
  identity_verified BOOLEAN NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (listing_id) REFERENCES listing (id)
);

CREATE TABLE calendar(
  id INT NOT NULL,
  listing_id INT NOT NULL,
  available BOOLEAN NOT NULL,
  price SMALLINT NOT NULL,
  adjusted_price SMALLINT NOT NULL,
  minimum_nights SMALLINT NOT NULL,
  maximum_nights SMALLINT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (listing_id) REFERENCES listing (id)
);
