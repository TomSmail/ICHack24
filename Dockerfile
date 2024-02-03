FROM starswap/ichackbase:v1
COPY ./ calendarapp
WORKDIR calendarapp
RUN pip install -r requirements.txt
CMD python index.py