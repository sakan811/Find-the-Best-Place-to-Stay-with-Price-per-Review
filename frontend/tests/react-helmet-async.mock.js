const React = require('react');

const Helmet = jest.createMockFromModule('react-helmet-async');

Helmet.HelmetProvider = ({ children }) => <>{children}</>;

module.exports = Helmet;
