import { ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface CardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
}

export function Card({ children, className, hover = true }: CardProps) {
  return (
    <div className={cn(
      'bg-white rounded-2xl border border-gray-100 p-6 shadow-sm overflow-hidden',
      hover && 'hover:shadow-xl hover:-translate-y-1 transition-all duration-300',
      className
    )}>
      {children}
    </div>
  );
}
