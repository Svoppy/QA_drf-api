import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = (__ENV.BASE_URL || 'http://localhost:8002').replace(/\/$/, '');
const STORE_URL = `${BASE_URL}/store`;
const SCENARIO = __ENV.SCENARIO || 'normal';

const SCENARIOS = {
  normal: {
    executor: 'constant-vus',
    vus: Number(__ENV.NORMAL_VUS || 5),
    duration: __ENV.NORMAL_DURATION || '3m',
  },
  load: {
    executor: 'constant-vus',
    vus: Number(__ENV.LOAD_VUS || 20),
    duration: __ENV.LOAD_DURATION || '5m',
  },
  peak: {
    executor: 'ramping-vus',
    stages: [
      { duration: __ENV.PEAK_RAMP_DURATION || '2m', target: Number(__ENV.PEAK_VUS || 50) },
      { duration: __ENV.PEAK_HOLD_DURATION || '3m', target: Number(__ENV.PEAK_VUS || 50) },
      { duration: __ENV.PEAK_RECOVERY_DURATION || '1m', target: 0 },
    ],
  },
  endurance: {
    executor: 'constant-vus',
    vus: Number(__ENV.ENDURANCE_VUS || 15),
    duration: __ENV.ENDURANCE_DURATION || '10m',
  },
};

if (!SCENARIOS[SCENARIO]) {
  throw new Error(`Unknown SCENARIO=${SCENARIO}. Use normal, load, peak, or endurance.`);
}

export const options = {
  scenarios: {
    [SCENARIO]: SCENARIOS[SCENARIO],
  },
  thresholds: {
    http_req_duration: [`p(95)<${Number(__ENV.P95_THRESHOLD_MS || 1200)}`],
    http_req_failed: [`rate<${Number(__ENV.ERROR_RATE_THRESHOLD || 0.05)}`],
    checks: ['rate>0.95'],
  },
};

const JSON_HEADERS = {
  headers: { 'Content-Type': 'application/json' },
  responseCallback: http.expectedStatuses({ min: 200, max: 399 }, 400, 404, 422),
  timeout: '10s',
};

function assertResponse(response, name, acceptedStatuses) {
  check(response, {
    [`${name}: accepted status`]: (r) => acceptedStatuses.includes(r.status),
    [`${name}: response under 10s`]: (r) => r.timings.duration < 10000,
  });
}

function catalogScenario() {
  const page = (__VU % 3) + 1;
  const productId = (__VU % Number(__ENV.PRODUCT_ID_SPAN || 30)) + 1;

  const productList = http.get(`${STORE_URL}/clothing-products/${page}/`, JSON_HEADERS);
  assertResponse(productList, 'product list', [200, 404]);

  const collections = http.get(`${STORE_URL}/clothing-collections/`, JSON_HEADERS);
  assertResponse(collections, 'collections list', [200]);

  const categories = http.get(`${STORE_URL}/categories/`, JSON_HEADERS);
  assertResponse(categories, 'categories list', [200]);

  const detail = http.get(`${STORE_URL}/clothing-products/items/${productId}/`, JSON_HEADERS);
  assertResponse(detail, 'product detail', [200, 404]);
}

function cartScenario() {
  const productId = (__VU % Number(__ENV.PRODUCT_ID_SPAN || 30)) + 1;
  const colorId = (__VU % Number(__ENV.COLOR_ID_SPAN || 8)) + 1;
  const token = `a3-k6-cart-${SCENARIO}-${__VU}-${__ITER}`;

  const createPayload = JSON.stringify({
    product: productId,
    principal_color: colorId,
    size: 'M',
    sleeve: 'None',
    quantity: (__ITER % 3) + 1,
    cart_token: token,
  });

  const create = http.post(`${STORE_URL}/product-variations/`, createPayload, JSON_HEADERS);
  assertResponse(create, 'product variation create', [201, 400, 404]);

  const cart = http.get(`${STORE_URL}/cart/${token}/`, JSON_HEADERS);
  assertResponse(cart, 'cart detail', [200, 404]);
}

function checkoutValidationScenario() {
  const response = http.post(`${STORE_URL}/orders/`, JSON.stringify({}), JSON_HEADERS);
  assertResponse(response, 'order validation failure', [400, 422]);
}

export default function () {
  const selector = Math.random();

  if (selector < 0.7) {
    catalogScenario();
  } else if (selector < 0.9) {
    cartScenario();
  } else {
    checkoutValidationScenario();
  }

  sleep(Number(__ENV.SLEEP_SECONDS || 1));
}

