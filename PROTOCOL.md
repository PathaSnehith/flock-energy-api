# Urja Meter Ops — Protocol Notes

## 1. Base URL

`https://urja-ops.flockenergy.tech`

## 2. Authentication

The portal requests use a session cookie:

`__Secure-better-auth.session_token`

The cookie is loaded from the `PORTAL_COOKIE` environment variable in `.env`. Requests may return HTTP 401 or 403 when the session is invalid or expired.

**Security:** Never commit `.env` or expose session cookies in logs or source control.

## 3. Discovered Endpoints

### Meter Search

- **Method:** GET
- **Path:** `/portal/meters/search`
- **Query parameters:**
  - `q`: search text
  - `page`: page number, starting at 1
- **Observed status:** HTTP 200

Example response structure:

```json
{
  "data": [
    {
      "meterId": "J100000",
      "serialNo": "SE33962",
      "make": "HPL",
      "phaseType": "single",
      "installStatus": "Decommissioned",
      "dtCode": "DT-001"
    }
  ],
  "total": 403,
  "page": 1,
  "pageSize": 20
}
```

The example shows the observed response structure; the full response contains additional records.

### Meter Energy

- **Method:** GET
- **Path:** `/portal/meters/{meter_id}/energy`
- **Example:** `/portal/meters/J100000/energy`
- **Observed status:** HTTP 200

The endpoint returns JSON. Record the exact response fields and their meanings after inspecting the response body.

## 4. Request Headers

The working Python client sends:

- `Accept: application/json, */*`
- `Referer: https://urja-ops.flockenergy.tech/meters`
- `Cookie: <session cookie>`

## 5. Error Handling

- HTTP 401 or 403: authentication rejected.
- Other unsuccessful portal responses: propagated as HTTP errors by the client.
- Non-JSON responses: reported as a runtime error.
- The FastAPI service currently maps portal failures to HTTP 502.

## 6. Investigation Limitations

- The meter search and energy endpoints were tested successfully.
- The individual meter-details endpoint has not yet been identified.
- The portal's full authentication flow has not been reverse-engineered; the implementation currently relies on a session cookie supplied through `.env`.
- The energy response schema still needs to be documented from the actual response.
