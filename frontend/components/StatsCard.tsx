'use client';

interface StatsCardProps {
  number: number | string;
  label: string;
  icon?: string;
  gradient?: string;
}

export default function StatsCard({ number, label, icon, gradient = 'from-blue-500 to-cyan-500' }: StatsCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 p-6 border border-gray-100">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm font-medium mb-2">{label}</p>
          <p className={`text-3xl font-bold bg-gradient-to-r ${gradient} bg-clip-text text-transparent`}>
            {number.toLocaleString()}
          </p>
        </div>
        {icon && (
          <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${gradient} flex items-center justify-center text-2xl`}>
            {icon}
          </div>
        )}
      </div>
    </div>
  );
}

