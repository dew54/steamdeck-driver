FROM python:3.11-slim

# Install pymavlink
RUN pip install pymavlink

# Create working directories
WORKDIR /work
RUN mkdir /output

# Copy your minimal.xml into the container
COPY minimal.xml /work/minimal.xml

# Command to generate the MAVLink headers
CMD ["python", "-m", "pymavlink.tools.mavgen", \
     "--lang=C", \
     "--wire-protocol=2.0", \
     "--output=/output", \
     "/work/minimal.xml"]
