'use client';

export default function Header() {
  return (
    <header className="bg-primary-500 text-white shadow-md">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-medium flex items-center gap-3">
              <span className="text-3xl">🌍</span>
              全球云基础设施节点分布图
            </h1>
            <p className="text-sm text-primary-50 mt-1 opacity-90">
              Cloud Infrastructure Node Distribution Map
            </p>
          </div>
          <div className="hidden md:flex items-center gap-2 text-sm">
            <span className="px-3 py-1 bg-white/20 text-white rounded-full backdrop-blur-sm">
              实时数据
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}

