/**
 * Custom NavbarItem component types for Docusaurus
 * Registers the custom-authNavbarItem type
 */

import ComponentTypes from '@theme-original/NavbarItem/ComponentTypes';
import AuthNavbarItem from './AuthNavbarItem';

export default {
  ...ComponentTypes,
  'custom-authNavbarItem': AuthNavbarItem,
};
