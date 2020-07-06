# Choosing what to do during your next vacation

In order to build the project you just need to execute:

`./docker/run.sh build`

Then, if you want to run the tests:

`./docker/run.sh test`

You can start the HTTP server by executing:

`./docker/run.sh start`

The server will be listening on port `5000`.

## Requesting Activities Information

```
curl -i -X GET \
 'http://localhost:5000/activities'
```

Use query params to filter out activities by: location, district and/or category:

```
curl -i -X GET \
 'http://localhost:5000/activities?location=outdoors&district=Centro&category=shopping'
```

## Requesting Recommended Activity
**NOTE**: For the sake of the exercise, consider `from_time` and `to_time` params mandatory. Otherwise `422` status code is returned.

```
curl -i -X GET \
 'http://localhost:5000/recommendation?category=shopping&from_time=16:30&to_time=20:30'
```

## Implementation Notes
- In order to apply the Dependency Inversion Principle, I have used the `Repository` pattern to make the HTTP endpoints depend on the abstraction instead of a concrete implementation. This way, switching from an *in file* implementation to a *database* one is just a matter of returning the specific instance from the `activities_repository` function you can find in the `http_resources.py` file. Ideally, the corresponding service would be instantiated from a Service Container that I didn't include to keep the code simpler.
- You can go through the commits log to follow the implementation approach in more detail and see how the solution has been evolving in baby steps thanks to the testing strategy applied.
- Ideally, the solution should not rely on a `.json` file, but a database. In that case, if we want to reach max performance, we could apply `CQRS` (Command Query Responsibility Segregation) to have a specialized table where activities are stored in their normalized shape (with each attribute as columns to be indexed and queried by) as well as followed by their GeoJSON representation to avoid that processing when querying results.
