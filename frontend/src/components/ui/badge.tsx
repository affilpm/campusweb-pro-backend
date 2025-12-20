import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

interface BadgeProps {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'outline';
  className?: string;
  icon?: boolean; // If true, adds a dot animation
}

export function Badge({ children, variant = 'primary', className, icon = false }: BadgeProps) {
  const variants = {
    primary: 'bg-blue-50 text-blue-700 border-blue-200',
    secondary: 'bg-gray-100 text-gray-700 border-gray-200',
    success: 'bg-green-50 text-green-700 border-green-200',
    warning: 'bg-amber-50 text-amber-700 border-amber-200',
    danger: 'bg-red-50 text-red-700 border-red-200',
    outline: 'bg-transparent border-gray-300 text-gray-500',
  };

  const dotColors = {
    primary: 'bg-blue-500',
    secondary: 'bg-gray-500',
    success: 'bg-green-500',
    warning: 'bg-amber-500',
    danger: 'bg-red-500',
    outline: 'bg-gray-400',
  };

  return (
    <span className={cn(
      'inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold border',
      variants[variant],
      className
    )}>
      {icon && (
        <span className={cn('w-2 h-2 rounded-full animate-pulse', dotColors[variant])} />
      )}
      {children}
    </span>
  );
}
