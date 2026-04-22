CREATE SCHEMA IF NOT EXISTS `steam_game_dlcs_schema` DEFAULT CHARACTER SET utf8mb3 ;
USE `steam_game_dlcs_schema` ;

CREATE TABLE IF NOT EXISTS `steam_game_dlcs_schema`.`games` (
  `game_id` INT NOT NULL,
  `game_url` VARCHAR(64) NOT NULL,
  `game_name` VARCHAR(64) NOT NULL,
  `game_cover` VARCHAR(192) NOT NULL,
  PRIMARY KEY (`game_id`),
  UNIQUE INDEX `game_id_UNIQUE` (`game_id` ASC) VISIBLE
);

CREATE TABLE IF NOT EXISTS `steam_game_dlcs_schema`.`dlcs` (
  `dlc_id` INT NOT NULL,
  `dlc_url` VARCHAR(64) NOT NULL,
  `dlc_name` VARCHAR(100) NOT NULL,
  `dlc_cover` VARCHAR(192) NOT NULL,
  `dlc_release_date` DATETIME NOT NULL,
  `dlc_actual_price` DECIMAL(4,2) NOT NULL,
  `dlc_access_date` DATETIME NOT NULL,
  `dlc_game_id` INT NOT NULL,
  PRIMARY KEY (`dlc_id`),
  UNIQUE INDEX `dlc_id_UNIQUE` (`dlc_id` ASC) VISIBLE,
  CONSTRAINT `fk_dlc_game`
    FOREIGN KEY (`dlc_game_id`)
    REFERENCES `steam_game_dlcs_schema`.`games` (`game_id`)
);
