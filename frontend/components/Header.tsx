'use client';

export default function Header() {
  return (
    <header className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white shadow-lg">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2 flex items-center gap-3">
              <span className="text-4xl">🌍</span>
              全球云基础设施节点分布图
            </h1>
            <p className="text-indigo-100 text-sm">
              Cloud Infrastructure Node Distribution Map
            </p>
          </div>
          <div className="hidden md:flex items-center gap-2 text-sm">
            <span className="px-3 py-1 bg-white/20 rounded-full backdrop-blur-sm">
              实时数据
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}

