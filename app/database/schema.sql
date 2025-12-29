--
-- PostgreSQL database dump
--

\restrict dDKSmf6Rvo7j4JMhK6LJrD7FQCSLrsgIU3pzKZ59EBMdKXBgptSu9Gw4LZq0rXf

-- Dumped from database version 16.10 (Debian 16.10-1.pgdg13+1)
-- Dumped by pg_dump version 16.10 (Debian 16.10-1.pgdg13+1)

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
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: video_snapshots; Type: TABLE; Schema: public; Owner: vluddexe
--

CREATE TABLE public.video_snapshots (
    id uuid NOT NULL,
    video_id uuid NOT NULL,
    views_count bigint NOT NULL,
    likes_count bigint NOT NULL,
    comments_count bigint NOT NULL,
    reports_count bigint NOT NULL,
    delta_views_count integer NOT NULL,
    delta_likes_count integer NOT NULL,
    delta_comments_count integer NOT NULL,
    delta_reports_count integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.video_snapshots OWNER TO vluddexe;

--
-- Name: videos; Type: TABLE; Schema: public; Owner: vluddexe
--

CREATE TABLE public.videos (
    id uuid NOT NULL,
    creator_id uuid NOT NULL,
    video_created_at timestamp with time zone NOT NULL,
    views_count bigint NOT NULL,
    likes_count bigint NOT NULL,
    comments_count bigint NOT NULL,
    reports_count bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.videos OWNER TO vluddexe;

--
-- Name: video_snapshots video_snapshots_pkey; Type: CONSTRAINT; Schema: public; Owner: vluddexe
--

ALTER TABLE ONLY public.video_snapshots
    ADD CONSTRAINT video_snapshots_pkey PRIMARY KEY (id);


--
-- Name: videos videos_pkey; Type: CONSTRAINT; Schema: public; Owner: vluddexe
--

ALTER TABLE ONLY public.videos
    ADD CONSTRAINT videos_pkey PRIMARY KEY (id);


--
-- Name: video_snapshots video_snapshots_video_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vluddexe
--

ALTER TABLE ONLY public.video_snapshots
    ADD CONSTRAINT video_snapshots_video_id_fkey FOREIGN KEY (video_id) REFERENCES public.videos(id);


--
-- PostgreSQL database dump complete
--

\unrestrict dDKSmf6Rvo7j4JMhK6LJrD7FQCSLrsgIU3pzKZ59EBMdKXBgptSu9Gw4LZq0rXf

