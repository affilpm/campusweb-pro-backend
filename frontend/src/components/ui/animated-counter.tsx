'use client';

import { motion, useInView, useSpring } from 'framer-motion';
import { useRef, useEffect, useState } from 'react';

interface AnimatedCounterProps {
  value: string;
  label: string;
  suffix?: string;
  className?: string;
}

export default function AnimatedCounter({ value, label, suffix = '', className = '' }: AnimatedCounterProps) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true });
  const [mounted, setMounted] = useState(false);
  const [displayValue, setDisplayValue] = useState('0');
  
  // Extract numeric part from value like "2000+" or "100"
  const numericValue = parseInt(value.replace(/[^0-9]/g, '')) || 0;
  const hasPlus = value.includes('+');

  const springValue = useSpring(0, { 
    stiffness: 50, 
    damping: 20,
    duration: 2000 
  });

  // Ensure consistent hydration by waiting for mount
  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (mounted && isInView) {
      springValue.set(numericValue);
    }
  }, [mounted, isInView, numericValue, springValue]);

  useEffect(() => {
    const unsubscribe = springValue.on('change', (latest) => {
      setDisplayValue(Math.floor(latest).toLocaleString());
    });
    return unsubscribe;
  }, [springValue]);

  // Render static value during SSR to prevent hydration mismatch
  const displayContent = mounted ? displayValue : '0';

  return (
    <div ref={ref} className={`text-center ${className}`}>
      <motion.div
        initial={{ scale: 0.5, opacity: 0 }}
        animate={isInView ? { scale: 1, opacity: 1 } : {}}
        transition={{ duration: 0.5, ease: 'easeOut' }}
        className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-amber-400 to-yellow-500 bg-clip-text text-transparent"
      >
        {displayContent}{hasPlus ? '+' : ''}{suffix}
      </motion.div>
      <p className="text-sm md:text-base text-blue-100 mt-2 font-medium">{label}</p>
    </div>
  );
}
