# Avant de pouvoir créer la base, il faut se connecter via root pour donner
# les droits à l'utilisateur 'lauredougui' sur cette nouvelle base.

# GRANT ALL PRIVILEGES ON healthier_food.* TO 'lauredougui'@'localhost';

CREATE DATABASE healthier_food CHARACTER SET 'utf8';
USE healthier_food;


CREATE TABLE History (
                history_id INT UNSIGNED AUTO_INCREMENT NOT NULL,
                request_date DATE NOT NULL,
                healthy_product_id INT NOT NULL,
                bad_product_id INT NOT NULL,
                PRIMARY KEY (history_id)
);


"""
CREATE TABLE Product (
                product_id INT UNSIGNED AUTO_INCREMENT NOT NULL,
                name VARCHAR(150) NOT NULL,
                description VARCHAR(100) NOT NULL,
                brand VARCHAR(30) NOT NULL,
                url VARCHAR(150) NOT NULL,
                store_id SMALLINT NOT NULL,
                nutriscore CHAR(1) NOT NULL,
                ingredients VARCHAR(500),
                energy_100g VARCHAR(5),
                allergens VARCHAR(300),
                traces VARCHAR(200),
                additives VARCHAR(300),
                label VARCHAR(150),
                PRIMARY KEY (product_id)
);
"""
CREATE TABLE Product (
                product_id INT UNSIGNED AUTO_INCREMENT NOT NULL,
                categories VARCHAR(150) NOT NULL,
                name VARCHAR(100) UNIQUE NOT NULL,
                description VARCHAR(100) NOT NULL,
                brand VARCHAR(100) UNIQUE NOT NULL,
                url VARCHAR(150) NOT NULL,
                store_id SMALLINT NOT NULL,
                nutriscore CHAR(1) NOT NULL,
                PRIMARY KEY (product_id)
);

CREATE TABLE Store (
                store_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
                name VARCHAR(50) UNIQUE NOT NULL,
                PRIMARY KEY (store_id)
);


CREATE TABLE Categorie (
                categorie_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
                name VARCHAR(150) NOT NULL,
                PRIMARY KEY (categorie_id)
);


CREATE TABLE Product_Categorie (
                product_id INT UNSIGNED NOT NULL,
                categorie_id SMALLINT UNSIGNED NOT NULL,
                PRIMARY KEY (product_id, categorie_id)
);


ALTER TABLE Product ADD CONSTRAINT store_product_fk
FOREIGN KEY (store_id)
REFERENCES Store (store_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE Product_Categorie ADD CONSTRAINT product_product_categorie_fk
FOREIGN KEY (product_id)
REFERENCES Product (product_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE Product_Categorie ADD CONSTRAINT categorie_product_categorie_fk
FOREIGN KEY (categorie_id)
REFERENCES Categorie (categorie_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;
