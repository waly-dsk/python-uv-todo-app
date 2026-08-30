CREATE TABLE public.todos (
    id uuid DEFAULT gen_random_uuid() NOT NULL,
    title text NOT NULL,
    content text,
    done boolean DEFAULT false NOT NULL,
    CONSTRAINT todos_pkey PRIMARY KEY (id)
);
