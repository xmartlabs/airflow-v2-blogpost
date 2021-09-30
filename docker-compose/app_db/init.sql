CREATE TABLE public.contacts (
  id INTEGER NOT NULL,
  email CHARACTER VARYING NOT NULL,
  first_name CHARACTER VARYING,
  last_name CHARACTER VARYING,
  hero_name CHARACTER VARYING,
  address CHARACTER VARYING,
  favorite_color CHARACTER VARYING,
  CONSTRAINT contacts_pkey PRIMARY KEY (id)
);

CREATE UNIQUE INDEX index_contacts_email
    ON public.contacts USING btree
    (email COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;

INSERT INTO public.contacts VALUES (1, 'miguel+spiderman@xmartlabs.com', 'Peter', 'Parker', 'Spiderman', '20 Ingram Street', 'red');
INSERT INTO public.contacts VALUES (2, 'miguel+ironman@xmartlabs.com', 'Tony', 'Stark', 'Ironman', '10880 Malibu Point', 'red & yellow');
INSERT INTO public.contacts VALUES (3, 'miguel+starlord@xmartlabs.com', 'Peter', 'Quill', 'Star-Lord', null, null);
INSERT INTO public.contacts VALUES (4, 'miguel+cap@xmartlabs.com', 'Steven', 'Rogers', 'Captain America', '569 Leaman Place', 'red & blue bars');
INSERT INTO public.contacts VALUES (5, 'miguel+hulk@xmartlabs.com', 'Bruce', 'Banner', 'Hulk', null, 'green');
