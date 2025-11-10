'use client';

interface StatsCardProps {
  number: number | string;
  label: string;
  icon?: string;
  gradient?: string;
}

export default function StatsCard({ number, label, icon, gradient = 'from-primary-500 to-primary-600' }: StatsCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md border border-neutral-200 p-6 hover:shadow-lg hover:border-primary-300 transition-all">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-neutral-500 mb-1">{label}</p>
          <p className="text-3xl font-semibold bg-gradient-to-r from-primary-500 to-primary-600 bg-clip-text text-transparent">
            {number.toLocaleString()}
          </p>
        </div>
        {icon && (
          <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-primary-500 to-primary-600 flex items-center justify-center text-2xl shadow-sm">
            {icon}
          </div>
        )}
      </div>
    </div>
  );
}

