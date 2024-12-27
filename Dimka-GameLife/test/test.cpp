#include "gtest/gtest.h"
#include "../lib/include/game_objects.hpp"
#include <stdexcept>
#include <set>

Field create_test_field(int width, int height, const std::vector<bool>& values) {
    Field field(width, height);
    field.set_field(values);
    return field;
}

TEST(FieldConstructors, DefaultConstructor) {
    Field field;
    ASSERT_EQ(field.get_width(), 3);
    ASSERT_EQ(field.get_height(), 3);
    ASSERT_EQ(field.get_field().size(), 9);
    for (bool cell : field.get_field()) {
        ASSERT_EQ(cell, false);
    }
}

TEST(FieldConstructors, CopyConstructor) {
    Field field1(5, 5, true);
    Field field2(field1);
    ASSERT_EQ(field1.get_width(), field2.get_width());
    ASSERT_EQ(field1.get_height(), field2.get_height());
    ASSERT_EQ(field1.get_field(), field2.get_field());
}

TEST(FieldConstructors, ParameterizedConstructor) {
    Field field(4, 5, true);
    ASSERT_EQ(field.get_width(), 4);
    ASSERT_EQ(field.get_height(), 5);
    ASSERT_EQ(field.get_field().size(), 20);
    for (bool cell : field.get_field()) {
        ASSERT_EQ(cell, true);
    }

    ASSERT_THROW(Field(2, 3), std::invalid_argument);
    ASSERT_THROW(Field(3, 2), std::invalid_argument);
}

TEST(FieldGetters, GetWidth) {
    Field field(5, 7);
    ASSERT_EQ(field.get_width(), 5);
}

TEST(FieldGetters, GetHeight) {
    Field field(5, 7);
    ASSERT_EQ(field.get_height(), 7);
}

TEST(FieldGetters, GetField) {
    Field field(3, 3, true);
    std::vector<bool> expected(9, true);
    ASSERT_EQ(field.get_field(), expected);
}

TEST(FieldGetters, GetNeighbours) {
    Field field = create_test_field(5, 5, {
        0, 1, 0, 1, 0,
        1, 1, 1, 1, 1,
        0, 1, 0, 1, 0,
        1, 1, 1, 1, 1,
        0, 1, 0, 1, 0
    });
    ASSERT_EQ(field.get_neighbours(1, 1), 4);
    ASSERT_EQ(field.get_neighbours(0, 0), 5);
    ASSERT_EQ(field.get_neighbours(2, 2), 8);
    ASSERT_EQ(field.get_neighbours(0, 2), 7);
    ASSERT_EQ(field.get_neighbours(4, 4), 5);
    ASSERT_EQ(field.get_neighbours(4, 2), 7);
    ASSERT_EQ(field.get_neighbours(2, 0), 7);
    ASSERT_EQ(field.get_neighbours(2, 4), 7);

}
TEST(FieldGetters, GetPoints) {
    Field field = create_test_field(3, 3, {
        1, 0, 1,
        0, 1, 0,
        1, 0, 1
    });

    std::vector<std::pair<int, int>> expected_points = {
        {0,0}, {0,2}, {1,1}, {2,0}, {2,2}
    };

    ASSERT_EQ(field.get_points(), expected_points);

    Field field2 = create_test_field(3, 3, {
        0, 0, 0,
        0, 0, 0,
        0, 0, 0
    });

    std::vector<std::pair<int, int>> expected_points2 = {};

    ASSERT_EQ(field2.get_points(), expected_points2);

}

TEST(FieldGetters, At) {
    Field field(3, 3);
    field.set_at(0, 1, true);
    ASSERT_TRUE(field.at(0, 1));
    ASSERT_FALSE(field.at(0, 0));

    // Test with wrapping
    ASSERT_TRUE(field.at(-3, 1));
    ASSERT_FALSE(field.at(-1, -1));

}

TEST(FieldSetters, SetAt) {
    Field field(3, 3);
    field.set_at(1, 2, true);
    ASSERT_TRUE(field.at(1, 2));
    field.set_at(1, 2, false);
    ASSERT_FALSE(field.at(1, 2));

    // Test with wrapping
    field.set_at(-1, 4, true);
    ASSERT_TRUE(field.at(2,1));
}

TEST(FieldSetters, SetField) {
    Field field(3, 3);
    std::vector<bool> new_field = {
        1, 0, 1,
        0, 1, 0,
        1, 0, 1
    };
    field.set_field(new_field);
    ASSERT_EQ(field.get_field(), new_field);

    std::vector<bool> bad_field = {1, 0};
    ASSERT_THROW(field.set_field(bad_field), std::invalid_argument);

    std::vector<bool> bad_field2 = {
        1, 0, 1,
        0, 1, 0,
        1, 0, 1,
        1
    };
    ASSERT_THROW(field.set_field(bad_field2), std::invalid_argument);

}

TEST(FieldEqual, EqualityOperator) {
    Field field1(3, 3, true);
    Field field2(3, 3, true);
    ASSERT_TRUE(field1 == field2);
    field2.set_at(0, 0, false);
    ASSERT_FALSE(field1 == field2);
}

//////////////////////////////////////////////////
//           UNIVERSE CLASS TESTS               //
//////////////////////////////////////////////////


TEST(UniverseConstructors, DefaultConstructor) {
    Universe universe;
    ASSERT_EQ(universe.get_name(), "Unknown");
    ASSERT_EQ(universe.get_birth(), (std::set<int>{3}));
    ASSERT_EQ(universe.get_survival(), (std::set<int>{2, 3}));
    ASSERT_EQ(universe.get_ticks(), 0);
}

TEST(UniverseConstructors, CopyConstructor) {
    Universe universe1("Test", (std::set<int>{1, 2}), (std::set<int>{3, 4}), 5, 5, true);
    Universe universe2(universe1);
    ASSERT_EQ(universe2.get_name(), "Test");
    ASSERT_EQ(universe2.get_birth(), (std::set<int>{1, 2}));
    ASSERT_EQ(universe2.get_survival(), (std::set<int>{3, 4}));
    ASSERT_EQ(universe2.get_field().get_width(), 5);
    ASSERT_EQ(universe2.get_field().get_height(), 5);
    ASSERT_NE(universe2.get_field().get_field().size(), 0);
    ASSERT_EQ(universe2.get_ticks(), 0);

    Universe universe3(universe2);
    ASSERT_EQ(universe3.get_name(), "Test");
    ASSERT_EQ(universe3.get_birth(), (std::set<int>{1,2}));
    ASSERT_EQ(universe3.get_survival(), (std::set<int>{3, 4}));
    ASSERT_EQ(universe3.get_field().get_width(), 5);
    ASSERT_EQ(universe3.get_field().get_height(), 5);
    ASSERT_NE(universe3.get_field().get_field().size(), 0);
    ASSERT_EQ(universe3.get_ticks(), 0);
}

TEST(UniverseConstructors, ParameterizedConstructor) {
    Universe universe(5, 7, true);
    ASSERT_EQ(universe.get_name(), "Unknown");
    ASSERT_EQ(universe.get_birth(), (std::set<int>{3}));
    ASSERT_EQ(universe.get_survival(), (std::set<int>{2, 3}));
    ASSERT_EQ(universe.get_field().get_width(), 5);
    ASSERT_EQ(universe.get_field().get_height(), 7);
    ASSERT_NE(universe.get_field().get_field().size(), 0);
    for (bool cell : universe.get_field().get_field()) {
        ASSERT_EQ(cell, true);
    }

    ASSERT_THROW(Universe(2, 3), std::invalid_argument);
    ASSERT_THROW(Universe(3, 2), std::invalid_argument);

    Universe universe2("Test", {1, 2}, {3, 4}, 4, 5, true);
    ASSERT_EQ(universe2.get_name(), "Test");
    ASSERT_EQ(universe2.get_birth(), (std::set<int>{1,2}));
    ASSERT_EQ(universe2.get_survival(), (std::set<int>{3, 4}));
    ASSERT_EQ(universe2.get_field().get_width(), 4);
    ASSERT_EQ(universe2.get_field().get_height(), 5);
    ASSERT_NE(universe2.get_field().get_field().size(), 0);
    for (bool cell : universe2.get_field().get_field()) {
        ASSERT_EQ(cell, true);
    }

    Field f(4, 5, true);
    Universe universe3("Test", {1, 2}, {3, 4}, f);
    ASSERT_EQ(universe3.get_name(), "Test");
    ASSERT_EQ(universe3.get_birth(), (std::set<int>{1,2}));
    ASSERT_EQ(universe3.get_survival(), (std::set<int>{3, 4}));
    ASSERT_EQ(universe3.get_field().get_width(), 4);
    ASSERT_EQ(universe3.get_field().get_height(), 5);
    ASSERT_NE(universe3.get_field().get_field().size(), 0);
    for (bool cell : universe3.get_field().get_field()) {
        ASSERT_EQ(cell, true);
    }
}

TEST(UniverseGetters, GetName) {
    Universe universe;
    ASSERT_EQ(universe.get_name(), "Unknown");
    universe.set_name("TestName");
    ASSERT_EQ(universe.get_name(), "TestName");
}

TEST(UniverseGetters, GetBirth) {
    Universe universe;
    ASSERT_EQ(universe.get_birth(), (std::set<int>{3}));
    universe.set_birth({1, 2});
    ASSERT_EQ(universe.get_birth(), (std::set<int>{1, 2}));
}

TEST(UniverseGetters, GetSurvival) {
    Universe universe;
    ASSERT_EQ(universe.get_survival(), (std::set<int>{2, 3}));
    universe.set_survival({4, 5});
    ASSERT_EQ(universe.get_survival(), (std::set<int>{4, 5}));
}
TEST(UniverseGetters, GetField) {
    Universe universe(3, 3, true);
    ASSERT_NE(universe.get_field().get_field().size(), 0);
}

TEST(UniverseGetters, GetTicks) {
    Universe universe;
    ASSERT_EQ(universe.get_ticks(), 0);
    universe.set_ticks(10);
    ASSERT_EQ(universe.get_ticks(), 10);
}

TEST(UniverseSetters, SetName) {
    Universe universe;
    universe.set_name("NewName");
    ASSERT_EQ(universe.get_name(), "NewName");
}

TEST(UniverseSetters, SetBirth) {
    Universe universe;
    universe.set_birth({1, 2, 3});
    ASSERT_EQ(universe.get_birth(), (std::set<int>{1, 2, 3}));
}

TEST(UniverseSetters, SetSurvival) {
    Universe universe;
    universe.set_survival({4, 5, 6});
    ASSERT_EQ(universe.get_survival(), (std::set<int>{4, 5, 6}));
}

TEST(UniverseSetters, SetField) {
    Universe universe(3, 3);
    Field new_field(3,3, true);
    universe.set_field(new_field);
    ASSERT_EQ(universe.get_field().get_field(), new_field.get_field());
}

TEST(UniverseSetters, SetCell) {
    Universe universe(3, 3);
    universe.set_cell(1, 1, true);
    ASSERT_TRUE(universe.get_field().at(1, 1));
    universe.set_cell(1, 1, false);
    ASSERT_FALSE(universe.get_field().at(1, 1));
}

TEST(UniverseSetters, SetCellError) {
    Universe universe(3, 3);

    universe.set_cell_err(1, 1, true);
    ASSERT_TRUE(universe.get_field().at(1, 1));

    ASSERT_THROW(universe.set_cell_err(1, 1, true), std::invalid_argument);

}

TEST(UniverseSetters, SetTicks) {
    Universe universe;
    universe.set_ticks(5);
    ASSERT_EQ(universe.get_ticks(), 5);
    ASSERT_THROW(universe.set_ticks(-1), std::invalid_argument);
}
TEST(UniverseTick, Tick) {
    Universe universe(3, 3);

    universe.set_cell(0, 1, true);
    universe.set_cell(1, 1, true);
    universe.set_cell(2, 1, true);

    ASSERT_EQ(universe.get_ticks(), 0);
    bool res = universe.tick();
    ASSERT_EQ(universe.get_ticks(), 1);
    ASSERT_FALSE(res);
}


int main(int argc, char** argv) {

    ::testing::InitGoogleTest(&argc, argv);

    return RUN_ALL_TESTS();
}
