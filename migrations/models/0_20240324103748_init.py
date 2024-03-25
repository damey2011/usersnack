from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "pizza" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "price" DECIMAL(10,2) NOT NULL,
    "images" VARCHAR[] NOT NULL
);
CREATE TABLE IF NOT EXISTS "pizza_extra" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL UNIQUE,
    "price" DECIMAL(10,2) NOT NULL
);
CREATE TABLE IF NOT EXISTS "pizza_extra_available_for" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_free" BOOL NOT NULL  DEFAULT False,
    "pizza_id" UUID NOT NULL REFERENCES "pizza" ("id") ON DELETE CASCADE,
    "pizza_extra_id" UUID NOT NULL REFERENCES "pizza_extra" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "pizza_extra_available_for" IS 'Defines the pizza options that are available to a particular pizza, and if they are';
CREATE TABLE IF NOT EXISTS "pizza_ingredient" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "pizza_recipe" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "ingredient_id" UUID NOT NULL REFERENCES "pizza_ingredient" ("id") ON DELETE CASCADE,
    "pizza_id" UUID NOT NULL REFERENCES "pizza" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_pizza_recip_pizza_i_86ca0d" UNIQUE ("pizza_id", "ingredient_id")
);
COMMENT ON TABLE "pizza_recipe" IS 'Can extend this model if there''s a need to specify other attributes like the';
CREATE TABLE IF NOT EXISTS "order" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "contact_phones" VARCHAR[] NOT NULL,
    "delivery_address" JSONB NOT NULL,
    "total_cost" DECIMAL(10,2) NOT NULL,
    "processed" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "order_package" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL  PRIMARY KEY,
    "order_id" UUID NOT NULL REFERENCES "order" ("id") ON DELETE CASCADE,
    "pizza_id" UUID NOT NULL REFERENCES "pizza" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "order_package_garnish" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "extra_id" UUID NOT NULL REFERENCES "pizza_extra" ("id") ON DELETE CASCADE,
    "order_package_id" UUID NOT NULL REFERENCES "order_package" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_order_packa_order_p_025964" UNIQUE ("order_package_id", "extra_id")
);
COMMENT ON TABLE "order_package_garnish" IS 'Can decide to put extra fields to specify other attributes, e.g. quantity of their extra';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
