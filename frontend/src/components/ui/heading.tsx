import { ReactNode } from 'react';
import { cn } from '@/lib/utils';

interface HeadingProps {
  title: string;
  subtitle?: string;
  align?: 'left' | 'center' | 'right';
  className?: string;
  badge?: ReactNode;
}

export function Heading({ title, subtitle, align = 'center', className, badge }: HeadingProps) {
  const alignments = {
    left: 'text-left',
    center: 'text-center mx-auto',
    right: 'text-right ml-auto',
  };

  return (
    <div className={cn('mb-12 md:mb-16', alignments[align], className)}>
      {badge && <div className="mb-4">{badge}</div>}
      <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 mb-4 tracking-tight leading-tight">
        {title}
      </h2>
      {subtitle && (
        <p className="text-lg md:text-xl text-gray-600 max-w-2xl leading-relaxed opacity-90 mx-auto">
          {subtitle}
        </p>
      )}
    </div>
  );
}
