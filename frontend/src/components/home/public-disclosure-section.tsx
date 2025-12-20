'use client';

interface GeneralInfoItem {
  id: number;
  title: string;
  value: string;
  order: number;
}

interface PublicDisclosureSectionProps {
  items: GeneralInfoItem[];
}

export default function PublicDisclosureSection({ items }: PublicDisclosureSectionProps) {
  if (!items || items.length === 0) {
    return null;
  }

  return (
    <section className="py-16 bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="container mx-auto px-4 max-w-4xl">
        {/* Section Header */}
        <div className="text-center mb-10">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-3">
            Public Disclosure
          </h2>
          <div className="w-20 h-1 bg-gradient-to-r from-blue-600 to-purple-600 mx-auto rounded-full"></div>
          <p className="text-gray-600 mt-4 max-w-2xl mx-auto">
            General information about our institution
          </p>
        </div>

        {/* Information Table */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
                  <th className="py-4 px-6 text-left text-sm font-semibold uppercase tracking-wider w-20">
                    Sl.No.
                  </th>
                  <th className="py-4 px-6 text-left text-sm font-semibold uppercase tracking-wider">
                    Information
                  </th>
                  <th className="py-4 px-6 text-left text-sm font-semibold uppercase tracking-wider">
                    Details
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {items.map((item, index) => (
                  <tr 
                    key={item.id} 
                    className="hover:bg-blue-50/50 transition-colors"
                  >
                    <td className="py-4 px-6 text-gray-900 font-semibold">
                      {index + 1}
                    </td>
                    <td className="py-4 px-6 text-gray-900 font-medium">
                      {item.title}
                    </td>
                    <td className="py-4 px-6 text-gray-600">
                      {item.value}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
}
