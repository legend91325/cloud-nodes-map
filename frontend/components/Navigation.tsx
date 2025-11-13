'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';

interface NavItem {
  label: string;
  href: string;
  children?: NavItem[];
}

const navigationItems: NavItem[] = [
  {
    label: '首页',
    href: '/',
  },
  {
    label: '服务',
    href: '/services',
    children: [
      {
        label: '全球基础设施',
        href: '/services/infrastructure',
      },
    ],
  },
  {
    label: '资讯',
    href: '/news',
  },
  {
    label: '关于',
    href: '/about',
  },
];

export default function Navigation() {
  const pathname = usePathname();
  const [activeDropdown, setActiveDropdown] = useState<string | null>(null);

  const isActive = (href: string) => {
    if (href === '/') {
      return pathname === '/';
    }
    return pathname.startsWith(href);
  };

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white border-b border-neutral-200 shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo 和网站名 */}
          <Link href="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
            <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white text-lg font-bold">云</span>
            </div>
            <span className="text-xl font-medium text-neutral-900">云计算指北</span>
          </Link>

          {/* 桌面端导航 */}
          <div className="hidden md:flex items-center gap-1">
            {navigationItems.map((item) => (
              <div
                key={item.href}
                className="relative"
                onMouseEnter={() => item.children && setActiveDropdown(item.href)}
                onMouseLeave={() => setActiveDropdown(null)}
              >
                <Link
                  href={item.href}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive(item.href)
                      ? 'text-primary-600 bg-primary-50'
                      : 'text-neutral-700 hover:text-primary-600 hover:bg-neutral-50'
                  }`}
                >
                  {item.label}
                  {item.children && (
                    <svg
                      className="inline-block ml-1 w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  )}
                </Link>

                {/* 下拉菜单 */}
                {item.children && activeDropdown === item.href && (
                  <div className="absolute top-full left-0 mt-1 w-48 bg-white rounded-lg shadow-lg border border-neutral-200 py-2">
                    {item.children.map((child, index) => (
                      <Link
                        key={`${child.href}-${index}`}
                        href={child.href}
                        className={`block px-4 py-2 text-sm transition-colors ${
                          isActive(child.href)
                            ? 'text-primary-600 bg-primary-50'
                            : 'text-neutral-700 hover:text-primary-600 hover:bg-neutral-50'
                        }`}
                      >
                        {child.label}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* 移动端菜单按钮 */}
          <button
            className="md:hidden p-2 text-neutral-700 hover:text-primary-600"
            onClick={() => setActiveDropdown(activeDropdown === 'mobile' ? null : 'mobile')}
            aria-label="菜单"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {activeDropdown === 'mobile' ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>

        {/* 移动端菜单 */}
        {activeDropdown === 'mobile' && (
          <div className="md:hidden border-t border-neutral-200 py-2">
            {navigationItems.map((item) => (
              <div key={item.href}>
                <Link
                  href={item.href}
                  className={`block px-4 py-2 text-sm font-medium ${
                    isActive(item.href)
                      ? 'text-primary-600 bg-primary-50'
                      : 'text-neutral-700'
                  }`}
                  onClick={() => setActiveDropdown(null)}
                >
                  {item.label}
                </Link>
                {item.children && (
                  <div className="pl-8">
                    {item.children.map((child, index) => (
                      <Link
                        key={`${child.href}-${index}`}
                        href={child.href}
                        className={`block px-4 py-2 text-sm ${
                          isActive(child.href)
                            ? 'text-primary-600 bg-primary-50'
                            : 'text-neutral-600'
                        }`}
                        onClick={() => setActiveDropdown(null)}
                      >
                        {child.label}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </nav>
  );
}

