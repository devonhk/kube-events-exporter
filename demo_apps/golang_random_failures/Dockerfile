FROM golang:1.16-alpine

EXPOSE 1323
WORKDIR /go/src/app
COPY . .
RUN go get -d -v ./...
RUN go install -v ./...
CMD ["golang_random_failures"]
