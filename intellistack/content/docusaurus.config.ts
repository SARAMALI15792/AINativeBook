import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'IntelliStack',
  tagline: 'AI-Native Learning Platform for Physical AI & Humanoid Robotics',
  favicon: 'img/favicon.ico',

  url: 'https://saramali15792.github.io',
  baseUrl: '/AINativeBook/docs/',
  projectName: 'AINativeBook',
  organizationName: 'SARAMALI15792',

  onBrokenLinks: 'ignore',
  markdown: {
    format: 'mdx',
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'ignore',
    },
  },

  // Custom fields for auth and backend integration
  customFields: {
    betterAuthUrl: process.env.BETTER_AUTH_URL || 'http://localhost:3001',
    backendUrl: process.env.BACKEND_URL || 'http://localhost:8000',
    frontendUrl: process.env.FRONTEND_URL || 'http://localhost:3000',
  },

  // Client modules for initialization
  clientModules: [
    './src/clientModules/authInit.ts',
  ],

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      en: {
        label: 'English',
        direction: 'ltr',
      },
      ur: {
        label: 'اردو',
        direction: 'rtl',
      },
    },
  },

  markdown: {
    format: 'mdx',
    mermaid: true,
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/intellistack/intellistack/tree/main/content/',
          showLastUpdateAuthor: true,
          showLastUpdateTime: true,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/intellistack-social-card.jpg',
    navbar: {
      title: 'IntelliStack',
      logo: {
        alt: 'IntelliStack Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          label: 'Home',
          href: '/AINativeBook/',
          position: 'left',
        },
        {
          type: 'docSidebar',
          sidebarId: 'stage1Sidebar',
          position: 'left',
          label: 'Stage 1',
        },
        {
          type: 'docSidebar',
          sidebarId: 'stage2Sidebar',
          position: 'left',
          label: 'Stage 2',
        },
        {
          type: 'docSidebar',
          sidebarId: 'stage3Sidebar',
          position: 'left',
          label: 'Stage 3',
        },
        {
          type: 'docSidebar',
          sidebarId: 'stage4Sidebar',
          position: 'left',
          label: 'Stage 4',
        },
        {
          type: 'docSidebar',
          sidebarId: 'stage5Sidebar',
          position: 'left',
          label: 'Stage 5',
        },
        {
          type: 'localeDropdown',
          position: 'right',
        },
        {
          type: 'custom-authNavbarItem',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Learning Path',
          items: [
            {
              label: 'Stage 1: Foundations',
              to: '/docs/stage-1/intro',
            },
            {
              label: 'Stage 2: ROS & Simulation',
              to: '/docs/stage-2/intro',
            },
            {
              label: 'Stage 3: Perception & Planning',
              to: '/docs/stage-3/intro',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'Documentation',
              to: '/docs/intro',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/intellistack/intellistack',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Forum',
              href: 'https://intellistack.example.com/community/forums',
            },
            {
              label: 'Study Groups',
              href: 'https://intellistack.example.com/community/groups',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} IntelliStack. Built with Docusaurus.`,
    },
    prism: {
      theme: require('prism-react-renderer').themes.github,
      darkTheme: require('prism-react-renderer').themes.dracula,
      additionalLanguages: ['python', 'bash', 'yaml', 'json'],
    },
    docs: {
      sidebar: {
        hideable: true,
        autoCollapseCategories: true,
      },
    },
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
  } satisfies Preset.ThemeConfig,

  themes: ['@docusaurus/theme-mermaid'],
};

export default config;
