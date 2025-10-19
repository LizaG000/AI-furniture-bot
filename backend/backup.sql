--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2 (Debian 15.2-1.pgdg110+1)
-- Dumped by pg_dump version 15.2 (Debian 15.2-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: __alembic_schema; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA __alembic_schema;


ALTER SCHEMA __alembic_schema OWNER TO postgres;

--
-- Name: db_schema; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA db_schema;


ALTER SCHEMA db_schema OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: __alembic_schema; Owner: postgres
--

CREATE TABLE __alembic_schema.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE __alembic_schema.alembic_version OWNER TO postgres;

--
-- Name: addresses; Type: TABLE; Schema: db_schema; Owner: postgres
--

CREATE TABLE db_schema.addresses (
    id uuid NOT NULL,
    id_user bigint NOT NULL,
    country character varying(255) NOT NULL,
    region character varying(255) NOT NULL,
    city character varying(255) NOT NULL,
    street character varying(255) NOT NULL,
    house_number character varying(10) NOT NULL,
    quadrature_number character varying(10) NOT NULL,
    postal_code integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE db_schema.addresses OWNER TO postgres;

--
-- Name: baskets; Type: TABLE; Schema: db_schema; Owner: postgres
--

CREATE TABLE db_schema.baskets (
    id uuid NOT NULL,
    id_user bigint NOT NULL,
    id_product uuid NOT NULL,
    count integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE db_schema.baskets OWNER TO postgres;

--
-- Name: categories; Type: TABLE; Schema: db_schema; Owner: postgres
--

CREATE TABLE db_schema.categories (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE db_schema.categories OWNER TO postgres;

--
-- Name: colors; Type: TABLE; Schema: db_schema; Owner: postgres
--

CREATE TABLE db_schema.colors (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE db_schema.colors OWNER TO postgres;

--
-- Name: colors_material; Type: TABLE; Schema: db_schema; Owner: postgres
--

CREATE TABLE db_schema.colors_material (
    id uuid NOT NULL,
    id_product uuid NOT NULL,
    id_color uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE db_schema.colors_material OWNER TO postgres;

--
-- Name: favorites; Type: TABLE; Schema: db_schema; Owner: postgres
--

CREATE TABLE db_schema.favorites (
    id uuid NOT NULL,
    id_user bigint NOT NULL,
    id_product uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE db_schema.favorites OWNER TO postgres;

--
-- Name: materials; Type: TABLE; Schema: db_schema; Owner: postgres
--

CREATE TABLE db_schema.materials (
    id uuid NOT NULL,
    name character varying(255) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE db_schema.materials OWNER TO postgres;

--
-- Name: orders; Type: TABLE; Schema: db_schema; Owner: postgres
--

CREATE TABLE db_schema.orders (
    id uuid NOT NULL,
    id_user bigint NOT NULL,
    id_addresses uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE db_schema.orders OWNER TO postgres;

--
-- Name: orders_products; Type: TABLE; Schema: db_schema; Owner: postgres
--

CREATE TABLE db_schema.orders_products (
    id uuid NOT NULL,
    id_order uuid NOT NULL,
    id_product uuid NOT NULL,
    count integer NOT NULL,
    price double precision NOT NULL,
    discount double precision NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE db_schema.orders_products OWNER TO postgres;

--
-- Name: products; Type: TABLE; Schema: db_schema; Owner: postgres
--

CREATE TABLE db_schema.products (
    id uuid NOT NULL,
    id_category uuid NOT NULL,
    name character varying(255) NOT NULL,
    description integer NOT NULL,
    count integer NOT NULL,
    price double precision NOT NULL,
    discount double precision NOT NULL,
    length double precision NOT NULL,
    height double precision NOT NULL,
    width double precision NOT NULL,
    images character varying(255)[] NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE db_schema.products OWNER TO postgres;

--
-- Name: products_materials; Type: TABLE; Schema: db_schema; Owner: postgres
--

CREATE TABLE db_schema.products_materials (
    id uuid NOT NULL,
    id_product uuid NOT NULL,
    id_material uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE db_schema.products_materials OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: db_schema; Owner: postgres
--

CREATE TABLE db_schema.users (
    id bigint NOT NULL,
    first_name character varying(255) NOT NULL,
    last_name character varying(255) NOT NULL,
    middle_name character varying(255),
    phone bigint NOT NULL,
    email character varying(200) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE db_schema.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: db_schema; Owner: postgres
--

CREATE SEQUENCE db_schema.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE db_schema.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: db_schema; Owner: postgres
--

ALTER SEQUENCE db_schema.users_id_seq OWNED BY db_schema.users.id;


--
-- Name: users id; Type: DEFAULT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.users ALTER COLUMN id SET DEFAULT nextval('db_schema.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: __alembic_schema; Owner: postgres
--

COPY __alembic_schema.alembic_version (version_num) FROM stdin;
97f343e4291e
\.


--
-- Data for Name: addresses; Type: TABLE DATA; Schema: db_schema; Owner: postgres
--

COPY db_schema.addresses (id, id_user, country, region, city, street, house_number, quadrature_number, postal_code, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: baskets; Type: TABLE DATA; Schema: db_schema; Owner: postgres
--

COPY db_schema.baskets (id, id_user, id_product, count, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: db_schema; Owner: postgres
--

COPY db_schema.categories (id, name, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: colors; Type: TABLE DATA; Schema: db_schema; Owner: postgres
--

COPY db_schema.colors (id, name, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: colors_material; Type: TABLE DATA; Schema: db_schema; Owner: postgres
--

COPY db_schema.colors_material (id, id_product, id_color, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: favorites; Type: TABLE DATA; Schema: db_schema; Owner: postgres
--

COPY db_schema.favorites (id, id_user, id_product, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: materials; Type: TABLE DATA; Schema: db_schema; Owner: postgres
--

COPY db_schema.materials (id, name, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: db_schema; Owner: postgres
--

COPY db_schema.orders (id, id_user, id_addresses, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: orders_products; Type: TABLE DATA; Schema: db_schema; Owner: postgres
--

COPY db_schema.orders_products (id, id_order, id_product, count, price, discount, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: db_schema; Owner: postgres
--

COPY db_schema.products (id, id_category, name, description, count, price, discount, length, height, width, images, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: products_materials; Type: TABLE DATA; Schema: db_schema; Owner: postgres
--

COPY db_schema.products_materials (id, id_product, id_material, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: db_schema; Owner: postgres
--

COPY db_schema.users (id, first_name, last_name, middle_name, phone, email, created_at, updated_at) FROM stdin;
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: db_schema; Owner: postgres
--

SELECT pg_catalog.setval('db_schema.users_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: __alembic_schema; Owner: postgres
--

ALTER TABLE ONLY __alembic_schema.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: addresses addresses_pkey; Type: CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.addresses
    ADD CONSTRAINT addresses_pkey PRIMARY KEY (id);


--
-- Name: baskets baskets_pkey; Type: CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.baskets
    ADD CONSTRAINT baskets_pkey PRIMARY KEY (id);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: colors_material colors_material_pkey; Type: CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.colors_material
    ADD CONSTRAINT colors_material_pkey PRIMARY KEY (id);


--
-- Name: colors colors_pkey; Type: CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.colors
    ADD CONSTRAINT colors_pkey PRIMARY KEY (id);


--
-- Name: favorites favorites_pkey; Type: CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.favorites
    ADD CONSTRAINT favorites_pkey PRIMARY KEY (id);


--
-- Name: materials materials_pkey; Type: CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.materials
    ADD CONSTRAINT materials_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: orders_products orders_products_pkey; Type: CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.orders_products
    ADD CONSTRAINT orders_products_pkey PRIMARY KEY (id);


--
-- Name: products_materials products_materials_pkey; Type: CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.products_materials
    ADD CONSTRAINT products_materials_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: addresses addresses_id_user_fkey; Type: FK CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.addresses
    ADD CONSTRAINT addresses_id_user_fkey FOREIGN KEY (id_user) REFERENCES db_schema.users(id);


--
-- Name: baskets baskets_id_product_fkey; Type: FK CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.baskets
    ADD CONSTRAINT baskets_id_product_fkey FOREIGN KEY (id_product) REFERENCES db_schema.products(id);


--
-- Name: baskets baskets_id_user_fkey; Type: FK CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.baskets
    ADD CONSTRAINT baskets_id_user_fkey FOREIGN KEY (id_user) REFERENCES db_schema.users(id);


--
-- Name: colors_material colors_material_id_color_fkey; Type: FK CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.colors_material
    ADD CONSTRAINT colors_material_id_color_fkey FOREIGN KEY (id_color) REFERENCES db_schema.colors(id);


--
-- Name: colors_material colors_material_id_product_fkey; Type: FK CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.colors_material
    ADD CONSTRAINT colors_material_id_product_fkey FOREIGN KEY (id_product) REFERENCES db_schema.products(id);


--
-- Name: favorites favorites_id_product_fkey; Type: FK CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.favorites
    ADD CONSTRAINT favorites_id_product_fkey FOREIGN KEY (id_product) REFERENCES db_schema.products(id);


--
-- Name: favorites favorites_id_user_fkey; Type: FK CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.favorites
    ADD CONSTRAINT favorites_id_user_fkey FOREIGN KEY (id_user) REFERENCES db_schema.users(id);


--
-- Name: orders orders_id_addresses_fkey; Type: FK CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.orders
    ADD CONSTRAINT orders_id_addresses_fkey FOREIGN KEY (id_addresses) REFERENCES db_schema.addresses(id);


--
-- Name: orders orders_id_user_fkey; Type: FK CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.orders
    ADD CONSTRAINT orders_id_user_fkey FOREIGN KEY (id_user) REFERENCES db_schema.users(id);


--
-- Name: orders_products orders_products_id_order_fkey; Type: FK CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.orders_products
    ADD CONSTRAINT orders_products_id_order_fkey FOREIGN KEY (id_order) REFERENCES db_schema.orders(id);


--
-- Name: orders_products orders_products_id_product_fkey; Type: FK CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.orders_products
    ADD CONSTRAINT orders_products_id_product_fkey FOREIGN KEY (id_product) REFERENCES db_schema.products(id);


--
-- Name: products products_id_category_fkey; Type: FK CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.products
    ADD CONSTRAINT products_id_category_fkey FOREIGN KEY (id_category) REFERENCES db_schema.categories(id);


--
-- Name: products_materials products_materials_id_material_fkey; Type: FK CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.products_materials
    ADD CONSTRAINT products_materials_id_material_fkey FOREIGN KEY (id_material) REFERENCES db_schema.materials(id);


--
-- Name: products_materials products_materials_id_product_fkey; Type: FK CONSTRAINT; Schema: db_schema; Owner: postgres
--

ALTER TABLE ONLY db_schema.products_materials
    ADD CONSTRAINT products_materials_id_product_fkey FOREIGN KEY (id_product) REFERENCES db_schema.products(id);


--
-- PostgreSQL database dump complete
--

