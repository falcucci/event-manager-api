# event-manager-api

POSTMAN           |  SWAGGER
:-------------------------:|:-------------------------:
[![Run in Postman](https://run.pstmn.io/button.svg)](https://api.postman.com/collections/3410852-4526f70b-1790-40da-906c-1bcd67f12b40?access_key=PMAT-01H06EEY1N1X86WB24YKANV42J ) |  [![Swagger logo](https://raw.githubusercontent.com/swagger-api/swagger-ui/master/dist/favicon-32x32.png)](http://localhost:8000/swagger/)

The event-manager-api is a rest API that provides an easy way to manage and track events.

It allows users to create, update, and delete events, as well as view and search them.

![code-snippet-7](https://github.com/falcucci/event-manager-api/assets/33763843/b02bb6d2-edb6-4ce6-989a-ea80b7cc4dbc)

## features

- [x] Users can register an account
- [x] Users can log in into their account
- [x] A system of token rotation is implemented. The API provides a user with access_token and a refresh_token, as well as a way to refresh and validate the access_token. The lifetime of the access_token is 1 hour and the lifetime of the refresh_token is 1 day
- [x] Users can create events in the app's database (postgres)
- [x] Users can see the list of events they have created
- [x] Users can see a list of all events
- [x] Users can edit the events they have created but not the ones created by other users
- [x] Users can register to an event or un-register. This can only be done in future events and not in past events.
- [x] Documentation
- [x] API docs (swagger or other)
- [ ] Tests
- [ ] Add logic to manage an event capacity: if event reaches maximum number of registered attendees, an error should be returned to a user trying to register
- [x] Add some filtering to endpoints retrieving events (e.g. date , type, status, past events, future events, etc)
- [x] Create a frontend to consume the API
