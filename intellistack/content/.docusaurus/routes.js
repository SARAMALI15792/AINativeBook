import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '13c'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '027'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '753'),
            routes: [
              {
                path: '/docs/stage-1/intro',
                component: ComponentCreator('/docs/stage-1/intro', '6c7'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/docs/stage-1/linux-fundamentals',
                component: ComponentCreator('/docs/stage-1/linux-fundamentals', 'a39'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/docs/stage-1/math-foundations',
                component: ComponentCreator('/docs/stage-1/math-foundations', '3c4'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/docs/stage-1/physics-basics',
                component: ComponentCreator('/docs/stage-1/physics-basics', '40f'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/docs/stage-1/python-basics',
                component: ComponentCreator('/docs/stage-1/python-basics', 'd73'),
                exact: true,
                sidebar: "stage1Sidebar"
              },
              {
                path: '/docs/stage-2/gazebo-simulation',
                component: ComponentCreator('/docs/stage-2/gazebo-simulation', '44d'),
                exact: true,
                sidebar: "stage2Sidebar"
              },
              {
                path: '/docs/stage-2/intro',
                component: ComponentCreator('/docs/stage-2/intro', '6ae'),
                exact: true,
                sidebar: "stage2Sidebar"
              },
              {
                path: '/docs/stage-2/ros2-setup',
                component: ComponentCreator('/docs/stage-2/ros2-setup', '9b7'),
                exact: true,
                sidebar: "stage2Sidebar"
              },
              {
                path: '/docs/stage-3/computer-vision',
                component: ComponentCreator('/docs/stage-3/computer-vision', '13e'),
                exact: true,
                sidebar: "stage3Sidebar"
              },
              {
                path: '/docs/stage-3/intro',
                component: ComponentCreator('/docs/stage-3/intro', 'f78'),
                exact: true,
                sidebar: "stage3Sidebar"
              },
              {
                path: '/docs/stage-4/intro',
                component: ComponentCreator('/docs/stage-4/intro', '8ce'),
                exact: true,
                sidebar: "stage4Sidebar"
              },
              {
                path: '/docs/stage-4/machine-learning-basics',
                component: ComponentCreator('/docs/stage-4/machine-learning-basics', '2b5'),
                exact: true,
                sidebar: "stage4Sidebar"
              },
              {
                path: '/docs/stage-5/intro',
                component: ComponentCreator('/docs/stage-5/intro', 'bfb'),
                exact: true,
                sidebar: "stage5Sidebar"
              },
              {
                path: '/docs/stage-5/project-guidelines',
                component: ComponentCreator('/docs/stage-5/project-guidelines', '73c'),
                exact: true,
                sidebar: "stage5Sidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', 'e5f'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
