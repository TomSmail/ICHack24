FROM python:latest
RUN git clone https://github.com/z3Prover/z3.git
RUN cd z3 && python scripts/mk_make.py -x
RUN cd z3/build && pip install z3-solver
RUN pip install -r requirements.txt
