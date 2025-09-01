--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

-- Started on 2025-09-01 18:40:34

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 223 (class 1259 OID 27542)
-- Name: disciplines; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.disciplines (
    discipline_code character varying(20) NOT NULL,
    discipline_name character varying(100) NOT NULL,
    theory_hours integer,
    practice_hours integer,
    independent_work_hours integer,
    course_project_hours integer,
    semester integer,
    CONSTRAINT disciplines_course_project_hours_check CHECK ((course_project_hours >= 0)),
    CONSTRAINT disciplines_independent_work_hours_check CHECK ((independent_work_hours >= 0)),
    CONSTRAINT disciplines_practice_hours_check CHECK ((practice_hours >= 0)),
    CONSTRAINT disciplines_semester_check CHECK ((semester > 0)),
    CONSTRAINT disciplines_theory_hours_check CHECK ((theory_hours >= 0))
);


ALTER TABLE public.disciplines OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 27509)
-- Name: education_form; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.education_form (
    education_form_id integer NOT NULL,
    education_form_name character varying(20)
);


ALTER TABLE public.education_form OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 27508)
-- Name: education_form_education_form_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.education_form_education_form_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.education_form_education_form_id_seq OWNER TO postgres;

--
-- TOC entry 4859 (class 0 OID 0)
-- Dependencies: 218
-- Name: education_form_education_form_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.education_form_education_form_id_seq OWNED BY public.education_form.education_form_id;


--
-- TOC entry 221 (class 1259 OID 27516)
-- Name: group_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.group_type (
    group_type_id integer NOT NULL,
    group_type_name character varying(20)
);


ALTER TABLE public.group_type OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 27515)
-- Name: group_type_group_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.group_type_group_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.group_type_group_type_id_seq OWNER TO postgres;

--
-- TOC entry 4860 (class 0 OID 0)
-- Dependencies: 220
-- Name: group_type_group_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.group_type_group_type_id_seq OWNED BY public.group_type.group_type_id;


--
-- TOC entry 222 (class 1259 OID 27522)
-- Name: groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.groups (
    group_number character varying(20) NOT NULL,
    specialty_code character varying(20),
    education_form_id integer,
    group_type_id integer
);


ALTER TABLE public.groups OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 27503)
-- Name: specialties; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.specialties (
    specialty_code character varying(20) NOT NULL,
    specialty_name character varying(100) NOT NULL
);


ALTER TABLE public.specialties OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 27562)
-- Name: teacher_workload; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teacher_workload (
    workload_id integer NOT NULL,
    teacher_id integer,
    discipline_code character varying(20),
    semester integer,
    hours integer,
    CONSTRAINT teacher_workload_hours_check CHECK ((hours > 0)),
    CONSTRAINT teacher_workload_semester_check CHECK ((semester > 0))
);


ALTER TABLE public.teacher_workload OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 27561)
-- Name: teacher_workload_workload_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.teacher_workload_workload_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.teacher_workload_workload_id_seq OWNER TO postgres;

--
-- TOC entry 4861 (class 0 OID 0)
-- Dependencies: 226
-- Name: teacher_workload_workload_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.teacher_workload_workload_id_seq OWNED BY public.teacher_workload.workload_id;


--
-- TOC entry 225 (class 1259 OID 27553)
-- Name: teachers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teachers (
    teacher_id integer NOT NULL,
    full_name character varying(100) NOT NULL,
    photo_path text
);


ALTER TABLE public.teachers OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 27552)
-- Name: teachers_teacher_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.teachers_teacher_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.teachers_teacher_id_seq OWNER TO postgres;

--
-- TOC entry 4862 (class 0 OID 0)
-- Dependencies: 224
-- Name: teachers_teacher_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.teachers_teacher_id_seq OWNED BY public.teachers.teacher_id;


--
-- TOC entry 4668 (class 2604 OID 27512)
-- Name: education_form education_form_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.education_form ALTER COLUMN education_form_id SET DEFAULT nextval('public.education_form_education_form_id_seq'::regclass);


--
-- TOC entry 4669 (class 2604 OID 27519)
-- Name: group_type group_type_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_type ALTER COLUMN group_type_id SET DEFAULT nextval('public.group_type_group_type_id_seq'::regclass);


--
-- TOC entry 4671 (class 2604 OID 27565)
-- Name: teacher_workload workload_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacher_workload ALTER COLUMN workload_id SET DEFAULT nextval('public.teacher_workload_workload_id_seq'::regclass);


--
-- TOC entry 4670 (class 2604 OID 27556)
-- Name: teachers teacher_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teachers ALTER COLUMN teacher_id SET DEFAULT nextval('public.teachers_teacher_id_seq'::regclass);


--
-- TOC entry 4849 (class 0 OID 27542)
-- Dependencies: 223
-- Data for Name: disciplines; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.disciplines (discipline_code, discipline_name, theory_hours, practice_hours, independent_work_hours, course_project_hours, semester) FROM stdin;
\.


--
-- TOC entry 4845 (class 0 OID 27509)
-- Dependencies: 219
-- Data for Name: education_form; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.education_form (education_form_id, education_form_name) FROM stdin;
\.


--
-- TOC entry 4847 (class 0 OID 27516)
-- Dependencies: 221
-- Data for Name: group_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.group_type (group_type_id, group_type_name) FROM stdin;
\.


--
-- TOC entry 4848 (class 0 OID 27522)
-- Dependencies: 222
-- Data for Name: groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.groups (group_number, specialty_code, education_form_id, group_type_id) FROM stdin;
\.


--
-- TOC entry 4843 (class 0 OID 27503)
-- Dependencies: 217
-- Data for Name: specialties; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.specialties (specialty_code, specialty_name) FROM stdin;
\.


--
-- TOC entry 4853 (class 0 OID 27562)
-- Dependencies: 227
-- Data for Name: teacher_workload; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.teacher_workload (workload_id, teacher_id, discipline_code, semester, hours) FROM stdin;
\.


--
-- TOC entry 4851 (class 0 OID 27553)
-- Dependencies: 225
-- Data for Name: teachers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.teachers (teacher_id, full_name, photo_path) FROM stdin;
\.


--
-- TOC entry 4863 (class 0 OID 0)
-- Dependencies: 218
-- Name: education_form_education_form_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.education_form_education_form_id_seq', 1, false);


--
-- TOC entry 4864 (class 0 OID 0)
-- Dependencies: 220
-- Name: group_type_group_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.group_type_group_type_id_seq', 1, false);


--
-- TOC entry 4865 (class 0 OID 0)
-- Dependencies: 226
-- Name: teacher_workload_workload_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.teacher_workload_workload_id_seq', 1, false);


--
-- TOC entry 4866 (class 0 OID 0)
-- Dependencies: 224
-- Name: teachers_teacher_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.teachers_teacher_id_seq', 1, false);


--
-- TOC entry 4688 (class 2606 OID 27551)
-- Name: disciplines disciplines_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.disciplines
    ADD CONSTRAINT disciplines_pkey PRIMARY KEY (discipline_code);


--
-- TOC entry 4682 (class 2606 OID 27514)
-- Name: education_form education_form_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.education_form
    ADD CONSTRAINT education_form_pkey PRIMARY KEY (education_form_id);


--
-- TOC entry 4684 (class 2606 OID 27521)
-- Name: group_type group_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.group_type
    ADD CONSTRAINT group_type_pkey PRIMARY KEY (group_type_id);


--
-- TOC entry 4686 (class 2606 OID 27526)
-- Name: groups groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (group_number);


--
-- TOC entry 4680 (class 2606 OID 27507)
-- Name: specialties specialties_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.specialties
    ADD CONSTRAINT specialties_pkey PRIMARY KEY (specialty_code);


--
-- TOC entry 4692 (class 2606 OID 27569)
-- Name: teacher_workload teacher_workload_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacher_workload
    ADD CONSTRAINT teacher_workload_pkey PRIMARY KEY (workload_id);


--
-- TOC entry 4690 (class 2606 OID 27560)
-- Name: teachers teachers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teachers
    ADD CONSTRAINT teachers_pkey PRIMARY KEY (teacher_id);


--
-- TOC entry 4693 (class 2606 OID 27532)
-- Name: groups groups_education_form_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_education_form_id_fkey FOREIGN KEY (education_form_id) REFERENCES public.education_form(education_form_id);


--
-- TOC entry 4694 (class 2606 OID 27537)
-- Name: groups groups_group_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_group_type_id_fkey FOREIGN KEY (group_type_id) REFERENCES public.group_type(group_type_id);


--
-- TOC entry 4695 (class 2606 OID 27527)
-- Name: groups groups_specialty_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.groups
    ADD CONSTRAINT groups_specialty_code_fkey FOREIGN KEY (specialty_code) REFERENCES public.specialties(specialty_code);


--
-- TOC entry 4696 (class 2606 OID 27575)
-- Name: teacher_workload teacher_workload_discipline_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacher_workload
    ADD CONSTRAINT teacher_workload_discipline_code_fkey FOREIGN KEY (discipline_code) REFERENCES public.disciplines(discipline_code);


--
-- TOC entry 4697 (class 2606 OID 27570)
-- Name: teacher_workload teacher_workload_teacher_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacher_workload
    ADD CONSTRAINT teacher_workload_teacher_id_fkey FOREIGN KEY (teacher_id) REFERENCES public.teachers(teacher_id);


-- Completed on 2025-09-01 18:40:34

--
-- PostgreSQL database dump complete
--

