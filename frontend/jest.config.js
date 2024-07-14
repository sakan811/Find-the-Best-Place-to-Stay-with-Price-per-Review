module.exports = {
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    "\\.(css|less|scss|sass)$": "<rootDir>/mocks/cssMock.js",
    "react-helmet-async": "<rootDir>/tests/react-helmet-async.mock.js"
  }
};
